import pandas as pd
from ta.momentum import RSIIndicator
import pandas_ta
from backend.scripts.other.standardization import standardization
#SAME

def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'
    # Generate signals based on SMA
    df.loc[df['1 Day RSI'] > 80, '1 Day Signals'] = 'Sell'
    df.loc[df['1 Day RSI'] < 20, '1 Day Signals'] = 'Buy'

    df.loc[df['1 Week RSI'] > 80, '1 Week Signals'] = 'Sell'
    df.loc[df['1 Week RSI'] < 20, '1 Week Signals'] = 'Buy'

    df.loc[df['1 Month RSI'] > 80, '1 Month Signals'] = 'Sell'
    df.loc[df['1 Month RSI'] < 20, '1 Month Signals'] = 'Buy'

    return df


def RSI(content):
    df = content.copy()

    df['1 Day RSI'] = RSIIndicator(close=df['Last trade price'], window=1).rsi()
    df['1 Week RSI'] = RSIIndicator(close=df['Last trade price'], window=7).rsi()
    df['1 Month RSI'] = RSIIndicator(close=df['Last trade price'], window=30).rsi()

    df = signals(df)

    return df








def RSI_pandas_ta(content):
    df = content.copy()

    df['1 Day RSI'] = pandas_ta.rsi(close=df['Last trade price'], length=1)
    df['1 Week RSI'] = pandas_ta.rsi(close=df['Last trade price'], length=7)
    df['1 Month RSI'] = pandas_ta.rsi(close=df['Last trade price'], length=30)


    df = signals(df)

    return df





def RSI_pandas(data: pd.DataFrame, days):
    data = data[['Date', 'Last trade price']]
    # data['Date'] = pd.to_datetime(data['Date'])
    delta = data['Last trade price'].diff(1)
    delta.dropna(inplace=True)

    positive = delta.copy()
    negative = delta.copy()

    positive[positive < 0] = 0
    negative[negative > 0] = 0

    avg_gain = positive.rolling(window=days).mean()
    avg_loss = abs(negative.rolling(window=days).mean())

    relative_strength = avg_gain / avg_loss

    RSI = 100.0 - (100.0 / (1.0 + relative_strength))
    data['RSI_pandas'] = RSI
    return data


#########################################################################################################################

import matplotlib.pyplot as plt

FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'

if __name__ == '__main__':
    data = pd.read_csv(f'{FOLDER}/KMB.csv')
    data = standardization(data)
    df1 = RSI(data)
    df2 = RSI_pandas_ta(data)
    print('---TA---')
    print(df1.info())
    print('---PANDAS_TA---')
    print(df2.info())
    # print(df1[['1 Day RSI', '1 Week RSI', '1 Month RSI']])
    # print(df2[['1 Day RSI', '1 Week RSI', '1 Month RSI']])
