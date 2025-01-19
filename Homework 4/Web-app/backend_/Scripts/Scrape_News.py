import re
import logging
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from Database.Database import Database

logging.basicConfig(level=logging.INFO)


# This is kinda messy
# This class is used to scrape news for the issuers and save the news to the database

class ScrapeNews:
    _db = None
    _name = None
    _automatic = []

    def __init__(self):
        self._db = Database()

    def _to_date(self, text):  # Is used to convert a text to a date
        try:
            date_obj = datetime.strptime(text, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
            return date_obj
        except ValueError as e:
            logging.error(f"\033[1;31mInvalid date format: {text} | Error: {e}\033[0m")
            return None

    def _contains_non_latin(self, text):  # Checks if a text contains letters that are not in the English alphabet
        return any(ord(char) > 127 for char in text)

    def _scrape_RSS_link(self, issuer):
        # Is used to scrape an URL from mse which contains and xml with all the links containing news for an issuer
        base_url = f'https://www.mse.mk/IssuerSelection/symbol/{issuer}'

        try:
            response = requests.get(base_url, timeout=(25, 60))
            soup = BeautifulSoup(response.text, 'html.parser')
            link_tag = soup.find("a", href=re.compile(r"^/IssuerSelection/rss/seinet/"))
            if link_tag:
                logging.info(f"Scraped MSE RSS link for \033[1;36m{issuer}\033[0m.")
                return 'https://www.mse.mk' + link_tag['href'].replace("IssuerSelection/", "")
        except:
            logging.info(f"Couldn't fetch the URL for issuer \033[1;36m{issuer}\033[0m. Exiting...")
            return None

        return None

    def _process_item(self, item):  # Processes the items from the xml file
        # https://api.seinet.com.mk/public/documents/single/70727 - api form used to scrape news
        # https://seinet.com.mk/document/70727 - normal form of the link from the xml item

        # To this base i only need to add the last part from both the regular link and the api
        base = 'https://api.seinet.com.mk/public/documents/single/'

        title = item.find('title').text
        parts = title.split(' - ', 2)

        if self._contains_non_latin(parts[1]):  # We check if the news contain text not in English
            return None

        self._name = parts[1]
        date_str = item.find('pubDate').text  # Extract the date from the xml item
        date_dt = self._to_date(date_str.strip())  # Convert it to a date
        if date_dt is None:
            return None

        link_str = item.find('link').text  # Extract the link from the item

        split_link = link_str.split('/')

        link = base + split_link[-1]

        return [date_dt.strftime('%m/%d/%Y'), link, '']

    def _extract_valid_rss_links(self, rss_url, issuer):  # Used to scrape the xml file
        if not rss_url:
            return []

        try:
            response = requests.get(rss_url, timeout=(25, 60))
            sp = BeautifulSoup(response.text, "lxml-xml")  # Takes the link that we scraped from mse
            items = sp.find_all('item')

            valid_list = []

            for item in items:
                res = self._process_item(item)
                if res is None:
                    continue
                valid_list.append(res)

            logging.info(f"Valid links extracted for \033[1;36m{issuer}\033[0m.")
            return valid_list
        except:
            logging.info(
                f"Error at scraping RSS links for issuer \033[1;36m{issuer}\033[0m.\n\n")
            return []

    def _parse_content(self, content):
        # Checks if the news contain automatically generated data
        # And parse the text that it gets form the api, it removes the HTML tags

        if self._name is None:
            return None

        FORBIDDEN = ['This is automaticaly generated document', 'This is an automatically generated information',
                     f'<p>{self._name} published', 'Non-audited',
                     f'<p>{self._name} published', f'<p>{self._name} publishes', f'<p>{self._name} informs that the',
                     ]

        for forbidden in FORBIDDEN:
            if forbidden in content:
                return None
        soup = BeautifulSoup(content, 'html.parser')

        # Extract all text, stripping out HTML tags
        text_content = soup.get_text(separator=' ', strip=True)

        return text_content

    def _scrape_link_logic(self, link, issuer):  # The scrape logic is here
        try:
            response = requests.get(link, timeout=(25, 60))

            # Check for a successful response
            if response.status_code == 200:
                # Parse the JSON data
                json_data = response.json()

                # Extract the 'data' part
                if 'data' in json_data:
                    data_part = json_data['data']

                    # Extract the 'content' from 'data'
                    if 'content' in data_part:
                        content = data_part['content']
                        result = self._parse_content(content)
                        if result is not None and result != '':
                            logging.info(f"Content extracted for : \033[34m{link}\033[0m.")
                            return result
                        else:
                            logging.info(
                                f"\033[33mAutomatic document for \033[1;36m{issuer}\033[0;33m detected: \033[34m{link}\033[33m.\033[0m")

                        # Do something with 'content' here, e.g., save it, process it
                    else:
                        logging.info("'content' key not found in the 'data' part.")

                else:
                    logging.info("The 'data' key was not found in the response.")

        except:
            logging.info(
                f"Couldn't get the content of \033[34m{link}\033[0m.")
            return None

        return None

    def _execute_scraping(self, links, issuer):  # Just calls the scrape logic for each issuer
        for link in links:
            logging.info(f"Scraping \033[34m{link[1]}\033[0m.")
            result = self._scrape_link_logic(link[1], issuer)
            link[2] = result

        logging.info(f"Scraping complete for \033[1;36m{issuer}\033[0m.\n\n")

    def _check(self, old, new):
        # Is used to check if the newly scraped links contain links that are already in the DB
        # So i keep track of the links that i previously used to scrape news
        # Then when the next time comes to scrape the news i check the links that needs to be scraped
        # I check if i already scraped them, if i did i just continue with the new ones

        # Handle edge cases
        if old is None or old.empty:
            logging.info("No existing data. All rows are considered new.")
            return [[], new]

        if not new:
            logging.info("No new data provided.")
            return [[], []]

        old.fillna('', inplace=True)
        old = old.values.tolist()
        old_dict = {tuple(row[:2]): row for row in old}  # Create a dictionary for quick lookups
        diff = []
        same = []

        for row in new:
            key = tuple(row[:2])  # Extract key (first two elements)
            if key in old_dict:
                # Append the matching row from old (full content)
                same.append(old_dict[key])
            else:
                # Append the row from new (with None)
                diff.append(row)

        return [same, diff]

    def _equality(self, first, second):
        # Checks if two link sets are identical

        for f, s in zip(first, second):  # Iterate through pairs of elements
            if f[:2] != s[:2]:  # Compare the first two elements
                return False
        return True

    def _scrape_implementation(self, issuers):

        for issuer in issuers:

            # Link that contains an xml, this xml contains links for where the news are published
            link = self._scrape_RSS_link(issuer)

            if link is None:
                continue

            # List of the links from the xml
            valid_links = self._extract_valid_rss_links(link, issuer)

            if not valid_links:
                logging.info(
                    f"Nothing to scrape for issuer \033[1;36m{issuer}\033[0m.\n\n")
                continue

            # Read the existing links form DB
            existing = self._db.read(issuer, 'news')

            # Check if the links from the xml are the same with the ones from DB
            if existing is not None and self._equality(existing.values.tolist(), valid_links):
                logging.info(
                    f"Links for issuer \033[1;36m{issuer}\033[0m are the same as the existing ones. Skipping.\n\n")
                continue


            elif existing is None:
                logging.info(
                    f"No news in the database for issuer \033[1;36m{issuer}\033[0m. Adding new links.")
                for_scrape_links = valid_links
            else:
                logging.info(f"New links found for issuer \033[1;36m{issuer}\033[0m. Updating database.")

                # Checks if some of the links are the same with the ones from DB
                updated_links = self._check(existing, valid_links)
                combined_links = updated_links[1] + updated_links[0]
                for_scrape_links = combined_links

            # Scraping the links from the xml
            self._execute_scraping(for_scrape_links, issuer)

            # Saving the links in DB
            self._db.save(issuer, 'news', for_scrape_links)

            # This is used in the _parse_content() method
            # It is used to check for automatically generated text
            self._name = None

    def start(self):
        print("STARTED SCRAPING NEWS")
        start_t = time.time()
        issuers = self._db.read('Issuers', 'stock')['Code'].values.tolist()
        self._scrape_implementation(issuers)
        print('TIME TAKEN TO SCRAPE NEWS: ', round((time.time() - start_t) / 60, 2), 'min  or ',
              round(time.time() - start_t, 2), 'sec')


if __name__ == '__main__':
    news = ScrapeNews()
    news.start()
