import pandas as pd

from backend.scripts.other.standardization import standardization


def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'

    df.loc[df['Last trade price'] > df['1 Day EMA'], '1 Day Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Day EMA'], '1 Day Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Week EMA'], '1 Week Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Week EMA'], '1 Week Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Month EMA'], '1 Month Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Month EMA'], '1 Month Signals'] = 'Sell'

    return df


def EMA(content):
    df = content.copy()

    df['1 Day EMA'] = df['Last trade price'].ewm(span=1, adjust=False).mean()
    df['1 Week EMA'] = df['Last trade price'].ewm(span=7, adjust=False).mean()
    df['1 Month EMA'] = df['Last trade price'].ewm(span=30, adjust=False).mean()
    # Initialize a column for signals
    df['Signal'] = 'Hold'

    df = signals(df)

    return df



if __name__ == '__main__':
    FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'
    data = pd.read_csv(f"{FOLDER}/KMB.csv")
    data = standardization(data)
    df = EMA(data)
    df.info()
    print(df[['1 Day EMA', '1 Week EMA', '1 Month EMA']].head(40))