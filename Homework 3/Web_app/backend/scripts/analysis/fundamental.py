import os
import re
import time
import logging
import requests
import pdfplumber
from datetime import datetime, timedelta
from langdetect import detect
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from transformers import pipeline

logging.basicConfig(level=logging.INFO)

# 1) Load model/pipeline once globally
# SENTIMENT_PIPELINE = pipeline("sentiment-analysis")



def parse_pdf(file_path: str) -> str:
    """Extract all text from a PDF file."""
    all_pages = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_pages.append(page_text.strip())
    return "\n".join(all_pages)



def sentiment_analysis(SENTIMENT_PIPELINE, text_list, pdf_text_list):
    data = text_list + pdf_text_list
    if not data:
        return [{'label': 'NEUTRAL-NO-NEWS', 'score': 0.5}]

    # Optionally chunk each text to 512, or let pipeline handle it if possible
    # But let's assume we pass them in as a list:
    results = SENTIMENT_PIPELINE(data, truncation=True)  # pass the entire list

    scores = [r['score'] for r in results]
    avg_score = sum(scores) / len(scores)

    sentiment = 'NEUTRAL'
    if avg_score > 0.6:
        sentiment = 'POSITIVE'
    elif avg_score < 0.4:
        sentiment = 'NEGATIVE'

    return [{'label': sentiment, 'score': avg_score}]


def check_language(text: str, sample_size=100) -> bool:
    sample = text[:sample_size] if len(text) > sample_size else text
    try:
        return detect(sample) == 'en'
    except:
        return False


def to_date(text):
    """Parse pubDate string to datetime."""
    return datetime.strptime(text, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)


def scrape_rss_link(issuer='KMB'):
    """Returns the RSS link for the issuer page."""
    base_url = f'https://www.mse.mk/IssuerSelection/symbol/{issuer}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_tag = soup.find("a", href=re.compile(r"^/IssuerSelection/rss/seinet/"))
    if link_tag:
        return 'https://www.mse.mk' + link_tag['href'].replace("IssuerSelection/", "")
    return None


def extract_rss_links(rss_url):
    """Extract item links from RSS feed in the last 14 days."""
    if not rss_url:
        return []
    rsp = requests.get(rss_url)
    sp = BeautifulSoup(rsp.text, "lxml-xml")
    items = sp.find_all('item')

    # Filter to last 14 days
    cutoff = datetime.now() - timedelta(days=14)
    valid_links = []
    for item in items:
        date_str = item.find('pubDate').text
        link_str = item.find('link').text
        if to_date(date_str) > cutoff:
            valid_links.append(link_str)
    return valid_links


def wait_for_non_empty_text(driver, css_selector, timeout=10):
    """
    Wait until the element with the given selector has non-empty text.
    Returns the WebElement if found, raises TimeoutException otherwise.
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )
    # Now wait until the element has non-empty text
    wait.until(lambda d: element.text.strip() != "")
    return element


def scrape_link(driver, link, download_dir):
    """
    Scrape a single link, returning [text, boolean_pdf].
    """
    additional_text = ''
    has_pdf = False

    try:
        driver.get(link)

        text_section = wait_for_non_empty_text(
            driver,
            css_selector=".text-left.ml-auto.mr-auto.col-md-11",
            timeout=10
        )

        content_div = text_section.find_element(By.XPATH, ".//div/div")
        raw_text = content_div.text.strip()

        # Check if automatically generated
        if raw_text.startswith('This is automaticaly generated document'):
            logging.info("Automatic document detected.")
            return ['', False]

        # Gather paragraphs
        paragraphs = content_div.find_elements(By.TAG_NAME, "p")
        additional_text = "\n".join(p.text.strip() for p in paragraphs)

        # Check language
        if not check_language(additional_text):
            logging.info("Text is not in English.")
            return ['', False]

        # Attempt file download
        dwd_button = wait_for_non_empty_text(
            driver,
            css_selector="[title^='Превземи датотека']",
            timeout=10
        )

        file_name = dwd_button.text.strip()
        if not file_name.lower().endswith('.pdf'):
            logging.info("Skipping non-PDF file.")
            return [additional_text, False]

        ActionChains(driver).move_to_element(dwd_button).click().perform()
        logging.info("Download initiated.")

        file_path = os.path.join(download_dir, file_name)
        start_time = time.time()
        while not os.path.exists(file_path):

            if time.time() - start_time > 5:  # wait up to 30s
                logging.info("File download timed out.")
                break

        if os.path.exists(file_path):
            logging.info(f"Download complete: {file_name}")
            has_pdf = True

    except Exception as exc:
        logging.error(f"Error during scraping {link}: {exc}", exc_info=True)
        return [additional_text, has_pdf]

    return [additional_text, has_pdf]



def ready_for_scrape(issuer, valid_links):
    """
    Prepare the Chrome WebDriver, scrape each link, return results.
    """
    download_dir = os.path.join(
        "d:\\", "Faculty", "5th Semester", "PYTHON",
        "backend", "scripts", "analysis", "News", issuer
    )

    os.makedirs(download_dir, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # other options for production usage...
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options)

    results = []
    try:
        for link in valid_links:
            logging.info(f"Scraping {link}")
            results.append(scrape_link(driver, link, download_dir))
    finally:
        driver.quit()

    logging.info("Scraping complete.")
    return results


def fundamental_main(issuer):
    """Main method to get RSS, scrape pages, and compute sentiment."""
    rss_url = scrape_rss_link(issuer)
    if not rss_url:
        logging.info("No RSS link found.")
        return ['NO-NEWS-AT-ALL', 0, '', '']

    valid_links = extract_rss_links(rss_url)
    logging.info(f"Found {len(valid_links)} links to process.")

    if not valid_links:
        return ['NEUTRAL-NO-NEWS', 0.5, '', '']

    data = ready_for_scrape(issuer, valid_links)

    text_list = []
    has_pdf = False
    for text_content, pdf_flag in data:
        text_list.append(text_content)
        if pdf_flag:
            has_pdf = True

    pdf_texts = []
    if has_pdf:
        download_dir = os.path.join(
            "d:\\", "Faculty", "5th Semester", "PYTHON",
            "backend", "scripts", "analysis", "News", issuer
        )
        files = os.listdir(download_dir)
        for f in files:
            full_path = os.path.join(download_dir, f)
            pdf_texts.append(parse_pdf(full_path))
            os.remove(full_path)

    # Check if there's any text at all
    if any(t for t in text_list) or pdf_texts:
        SENTIMENT_PIPELINE = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = sentiment_analysis(SENTIMENT_PIPELINE, text_list.copy(), pdf_texts.copy())
        sentiment_label = result[0]['label']
        sentiment_score = result[0]['score']

        # Combine text
        text_container = "\n".join(t for t in text_list if t)
        pdf_container = "\n".join(pdf_texts)

        return [sentiment_label, sentiment_score, text_container, pdf_container]

    return ['NO-NEWS-AT-ALL', 0, '', '']


st_time = time.time()

if __name__ == '__main__':
    print(fundamental_main('ALK'))
    print(f'END:  {time.time() - st_time}')