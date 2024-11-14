import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import os
from threading import Thread


# Filter 1: Automatically retrieve all issuers from the Macedonian Stock Exchange
def fetch_issuers():
    # The URL that we use to fetch the issuers
    url = 'https://www.mse.mk/en/stats/symbolhistory/KMB'

    # request
    response = requests.get(url)

    # In case if the requests fails
    while response.status_code != 200:
        response = requests.get(url)

    # Parse the HTML that we got
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the dropdown menu for issuers
    issuers_dropdown = soup.find('select', {'id': 'Code'})
    issuers = []

    # Add the issuer code to the issuers list
    for option in issuers_dropdown.find_all('option'):
        code = option.get('value')
        if code and not any(char.isdigit() for char in code):
            issuers.append(code)

    # return the issuers
    return issuers


# Function to create a DataFrame from a list of data
def table(data):
    # Converting a list in to a Dataframe
    if (data):
        df = pd.DataFrame(data)
        df.columns = ["Date", "Last trade price", "Max", "Min", "Avg.Price", "%chg.", "Volume",
                      "Turnover in BEST in denars", "Total turnover in denars"]
        return df
    return None


# Helper function to parse individual table rows
def parse_cells(row):
    # This is used to switch the ',' -> '.' and vise versa
    translation_table = str.maketrans({',': '.', '.': ','})

    # Finds the cells for a given row
    cells = row.find_all('td')

    if len(cells) < 9:
        return None

    # Parsing
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


# Function to parse the HTML soup and extract table data
def parse_soup(bs):
    # Finds all the table bodys
    table = bs.find_all('tbody')

    # Check if the length is zero if it is it returns None
    if len(table) == 0:
        return None

    table = table[0]

    # Finds all rows of the table
    rows = table.find_all('tr')
    res = []

    # Iterates through the table
    for row in rows:
        # Appends the parsed cells tho the res variable
        res.append(parse_cells(row))

    # In the end we return the res variable
    # that contains all the data of the table
    return res


# Helper function to calculate the date range in days
def range_in_days(date, days):
    # Calculates the date that is x (days) days ago
    start_date = datetime.strptime(date, '%m/%d/%Y') - timedelta(days=days)
    return start_date.strftime('%m/%d/%Y')


# Filter 3: Fetch missing data for an issuer
def fetch_range(companies, code, start_date, end_date):
    # Our base URL
    base_url = 'https://www.mse.mk/en/stats/symbolhistory/'

    # The start date
    date_from = datetime.strptime(start_date, '%m/%d/%Y')

    # The end date
    date_to = datetime.strptime(end_date, '%m/%d/%Y')

    # The days between the starting and the ending day
    days = (date_to - date_from).days

    # The total years between the two dates
    years = days // 365

    # The days left from the year for example 2 years and 28 days
    # The 28 in this case represents the daysleft
    daysleft = days % 365

    start_date = range_in_days(end_date, 365)

    if years == 0:
        # If there are 0 years we just calculate the date that is 'daysleft' away
        start_date = range_in_days(end_date, daysleft)

    # Variable for saving the data
    stock_data = []

    # We go in a for loop from 1 to years + 1 to include the days left
    for i in range(1, years + 2):
        if i == (years + 1):
            # If i == years + 1 then we calculate the date that is 'daysleft' away
            start_date = datetime.strptime(end_date, '%m/%d/%Y') - timedelta(days=daysleft)
            start_date = date_from.strftime('%m/%d/%Y').__str__()

        # Our URL
        url = base_url + code

        # A form data that contains the start date and the end date
        form_data = {
            'FromDate': start_date,
            'ToDate': end_date,
        }

        # The response for the request
        response = requests.post(url, data=form_data, timeout=(25, 60))

        while response.status_code != 200:
            # We sent repeted requests if the status is not 200 (OK)
            response = requests.post(url, data=form_data, timeout=(25, 60))

        # We use Beautifulsoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # We parse the data with the parse_soup(bs) method
        parsed = parse_soup(soup)

        if parsed is not None:
            stock_data += parsed

        # We set the end date to the start date
        end_date = start_date

        # We set the start date one year back
        start_date = range_in_days(end_date, 365)

    # We transform the data in to a Dataframe
    res = table(stock_data)

    # Save it to Excel
    res.to_excel(f'./database/{code}.xlsx', index=False)
    companies[code] = res


# Filter 2: Check and update the last date of available data
def fetch_data(companies, issuers):
    dataframes = dict()
    threads = []

    # The date of today
    today = str(datetime.today().strftime('%m/%d/%Y'))

    for code in issuers:

        if f'{code}.xlsx' not in os.listdir('./database'):
            # If we can't find the corresponding file for a given issuer then we set the search_from to 10 years ago
            search_from = range_in_days(today, 365 * 10)
        else:
            # We import the file from the database
            issuer_df = pd.read_excel(f'./database/{code}.xlsx')

            # We search for the last date of data
            search_from = str(
                (datetime.strptime(issuer_df.Date[0], '%m/%d/%Y') + timedelta(days=1)).strftime('%m/%d/%Y'))
            yesterday = (datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y')

            # We check if the last date of data if it is today or yesterday we continue
            if today == search_from or yesterday == search_from:
                continue

            # Adds the issuers_df to dataframes under the key code and drops the unnamed
            dataframes[code] = issuer_df

            # Use of threads
        thread = Thread(target=fetch_range, args=(companies, code, search_from, today))
        thread.start()
        threads.append(thread)

    for thread in threads:
        # Joining the threads
        thread.join()

    for code in issuers:
        # if the code is a key to the companies
        if code in companies:
            # Get the existing DataFrame for the issuer code, or use an empty DataFrame if not available
            new_data = pd.DataFrame()
            if code in dataframes:
                new_data = dataframes[code]

            # Concatenate the existing and new data along the rows (axis=0)
            df = pd.concat([companies[code], new_data], axis=0)

            # Save the DataFrame to a Excel file in the 'database' folder, named after the company code
            df.to_excel(f'./database/{code}.xlsx', index=False)


# Main Pipeline
if __name__ == '__main__':
    issuers = fetch_issuers()
    companies = dict()
    fetch_data(companies, issuers)


