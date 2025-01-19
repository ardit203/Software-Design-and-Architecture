import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from threading import Thread, Lock
import time
from Database.Database import Database


# Used to scrape stock data
class ScrapeStockData:
    _db = None
    _issuers = None
    _last_dates = None
    _lock = None

    def __init__(self):
        self._db = Database()
        self._issuers = list()
        self._last_dates = list()
        self._lock = Lock()

    def fetch_prediction_issuers(self):
        url = 'https://www.mse.mk/en/stats/top-ten-listed-shares'

        response = requests.get(url)

        while response.status_code != 200:
            response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        td_elements_with_links = soup.find_all('td')
        codes = []
        # Extract and print the href and text from each <a> tag
        for td in td_elements_with_links:
            a_tag = td.find('a')
            if a_tag and not any(char.isdigit() for char in a_tag.text):
                text = a_tag.text
                codes.append(text)

        self._db.save('Prediction', 'prediction', pd.DataFrame(codes, columns=['Code']))

    def _fetch_issuers(self):
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
        self._db.save('Issuers', 'stock', issuers)
        return issuers

    def _parse_cells(self, row):
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

    def _parse_soup(self, bs):
        table = bs.find_all('tbody')

        if len(table) == 0:
            return None

        table = table[0]

        rows = table.find_all('tr')
        res = []

        for row in rows:
            res.append(self._parse_cells(row))

        return res

    def _range_in_days(self, date_str, days):
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        new_date = date_obj - timedelta(days=days)
        return new_date.strftime('%m/%d/%Y')

    def _request_HTTP(self, code, start_date, end_date):
        base_url = 'https://www.mse.mk/en/stats/symbolhistory/'
        url = base_url + code + "?" + "FromDate=" + start_date + '&ToDate=' + end_date

        retries = 5
        for _ in range(retries):
            try:
                response = requests.post(url, timeout=(25, 60))
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                res = self._parse_soup(soup)
                return res
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying...")
                time.sleep(1)
        print(f"Failed to fetch data for {code} after {retries} attempts.")
        return None

    def _fetch_range(self, code, start_date, end_date):
        start_date_obj = datetime.strptime(start_date, '%m/%d/%Y')
        end_date_obj = datetime.strptime(end_date, '%m/%d/%Y')

        stock_data = []
        while end_date_obj > start_date_obj:
            fetch_start = max(start_date_obj, end_date_obj - timedelta(days=365))
            parsed = self._request_HTTP(code, fetch_start.strftime('%m/%d/%Y'), end_date_obj.strftime('%m/%d/%Y'))

            if parsed:
                stock_data += parsed

            end_date_obj = fetch_start - timedelta(days=1)


        if stock_data:
            last = stock_data[0][0]
            with self._lock:  # Thread-safe update of shared resource
                self._last_dates.append([code, last])
                self._db.save(code, 'stock', stock_data)
                self._db.save(code, 'std', stock_data)

    def _fetch_data(self, issuers):
        threads = []
        today = (datetime.today()).strftime('%m/%d/%Y')
        # today = (datetime.today() - timedelta(days=20)).strftime('%m/%d/%Y')
        last_date_flag = True
        last_dates = None

        for code in issuers:

            if not self._db.exists(code, 'stock'):
                search_from = self._range_in_days(today, 365 * 10.5)
            else:
                if last_date_flag:
                    last_date_flag = False
                    last_dates = self._db.read('LastDates', 'stock')

                search_pair = last_dates.loc[last_dates['Code'] == code].values[0]
                search_from = last_dates.loc[last_dates['Code'] == code, 'Date'].values[0]

                print('Search Pair: ',search_pair)

                search_from = (datetime.strptime(search_from, '%m/%d/%Y') + timedelta(days=1)).strftime('%m/%d/%Y')

                print(search_from)
                if today == search_from:
                    continue

            # self._fetch_range(code,search_from,today)
            thread = Thread(target=self._fetch_range, args=(code, search_from, today))
            thread.start()
            threads.append(thread)


        for thread in threads:
            thread.join()

        if last_date_flag:
            self._db.save('LastDates', 'stock', self._last_dates)
        else:
            self._db.save('LastDates', 'stock', last_dates)



    def start(self):
        print("STARTED SCRAPING STOCK DATA")
        start_t = time.time()
        self.fetch_prediction_issuers()
        issuers = self._fetch_issuers()
        self._fetch_data(issuers)
        print('TIME TAKEN TO SCRAPE STOCK DATA: ', round((time.time() - start_t) / 60, 2), 'min  or ',
              round(time.time() - start_t, 2), 'sec')


if __name__ == '__main__':
    scraper = ScrapeStockData()
    scraper.start()