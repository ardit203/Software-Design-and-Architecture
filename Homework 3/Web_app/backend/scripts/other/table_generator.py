from datetime import datetime
import pandas as pd
from backend.scripts.other.standardization import fill

FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'

def create_table(issuer, from_date, to_date):
    from_date = datetime.strptime(from_date, '%Y-%m-%d')

    to_date = datetime.strptime(to_date, '%Y-%m-%d')


    df = pd.read_csv(f"{FOLDER}/{issuer}.csv")
    df.fillna(' ', inplace=True)


    df['Date'] = pd.to_datetime(df['Date'])
    # Filter data within the date range
    if from_date:
        df = df[df['Date'] >= from_date]
    if to_date:
        df = df[df['Date'] <= to_date]

    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    return df