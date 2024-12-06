import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import os
from threading import Thread
import time


def fetch_issuers():
    url = 'https://www.mse.mk/en/stats/symbolhistory/KMB'
    response = requests.get(url)

    while response.status_code != 200:
        response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    issuers_dropdown = soup.find('select', {'id': 'Code'})
    issuers = []

    for option in issuers_dropdown.find_all('option'):
        code = option.get('value')
        if code and not any(char.isdigit() for char in code):
            issuers.append(code)
    pd.DataFrame(issuers, columns=['Code']).to_csv('database/Issuers.csv', index=False)
    return issuers


def table(data):
    if (data):
        df = pd.DataFrame(data)
        df.columns = ["Date", "Last trade price", "Max", "Min", "Avg.Price", "%chg.", "Volume",
                      "Turnover in BEST in denars", "Total turnover in denars"]
        return df
    return None


def parse_cells(row):
    translation_table = str.maketrans({',': '.', '.': ','})

    cells = row.find_all('td')

    if len(cells) < 9:
        return None

    date = cells[0].text
    last_trade_price = cells[1].text.translate(translation_table)
    max = cells[2].text.translate(translation_table)
    min = cells[3].text.translate(translation_table)
    avg_price = cells[4].text.translate(translation_table)
    chg = cells[5].text.translate(translation_table)
    volume = cells[6].text.translate(translation_table)
    turnover_in_best = cells[7].text.translate(translation_table)
    total_turnover = cells[8].text.translate(translation_table)

    result = [date, last_trade_price, max, min, avg_price, chg, volume, turnover_in_best, total_turnover]
    return result


def parse_soup(bs):
    table = bs.find_all('tbody')

    if len(table) == 0:
        return None

    table = table[0]

    rows = table.find_all('tr')
    res = []

    for row in rows:
        res.append(parse_cells(row))

    return res


def range_in_days(date_str, days):
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    new_date = date_obj - timedelta(days=days)
    return new_date.strftime('%m/%d/%Y')


def request_HTTP(code, start_date, end_date):
    base_url = 'https://www.mse.mk/en/stats/symbolhistory/'
    url = base_url + code + "?" + "FromDate=" + start_date + '&ToDate=' + end_date

    retries = 5
    for _ in range(retries):
        try:
            response = requests.post(url, timeout=(25, 60))
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return parse_soup(soup)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(1)
    print(f"Failed to fetch data for {code} after {retries} attempts.")
    return None


def fetch_range(companies, code, start_date, end_date):
    start_date_obj = datetime.strptime(start_date, '%m/%d/%Y')
    end_date_obj = datetime.strptime(end_date, '%m/%d/%Y')

    stock_data = []
    while end_date_obj > start_date_obj:
        fetch_start = max(start_date_obj, end_date_obj - timedelta(days=365))
        parsed = request_HTTP(code, fetch_start.strftime('%m/%d/%Y'), end_date_obj.strftime('%m/%d/%Y'))

        if parsed:
            stock_data += parsed

        end_date_obj = fetch_start - timedelta(days=1)

    if stock_data:
        res = table(stock_data)
        companies[code] = res
        os.makedirs('database', exist_ok=True)
        res.to_csv(f'database/{code}.csv', index=False)


def fetch_data(companies, issuers):
    threads = []
    dataframes = dict()
    today = (datetime.today() - timedelta(days=26)).strftime('%m/%d/%Y')

    for code in issuers:

        if f'{code}.csv' not in os.listdir('database'):
            search_from = range_in_days(today, 365 * 10)
        else:
            issuer_df = pd.read_csv(f'database/{code}.csv')
            search_from = (datetime.strptime(issuer_df.Date.iloc[0], '%m/%d/%Y') + timedelta(days=1)).strftime(
                '%m/%d/%Y')
            yesterday = (datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y')

            if today == search_from or yesterday == search_from:
                continue

            dataframes[code] = issuer_df

        thread = Thread(target=fetch_range, args=(companies, code, search_from, today))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for code in issuers:

        if code in companies.keys():

            new_data = pd.DataFrame()
            if code in dataframes:
                new_data = dataframes[code]

            df = pd.concat([companies[code], new_data], axis=0)
            df.to_csv(f'database/{code}.csv', index=False)


if __name__ == '__main__':
    issuers = fetch_issuers()
    companies = dict()
    fetch_data(companies, issuers)
