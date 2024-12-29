import pandas as pd
from ta.trend import WMAIndicator
import pandas_ta
import numpy as np
# SAME SAME
from backend.scripts.other.standardization import standardization


def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'

    df.loc[df['Last trade price'] > df['1 Day WMA'], '1 Day Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Day WMA'], '1 Day Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Week WMA'], '1 Week Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Week WMA'], '1 Week Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Month WMA'], '1 Month Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Month WMA'], '1 Month Signals'] = 'Sell'

    return df



# WMA using pandas_ta
def WMA(content):
    df = content.copy()

    df['1 Day WMA'] = pandas_ta.wma(close=df['Last trade price'], length=1)
    df['1 Week WMA'] = pandas_ta.wma(close=df['Last trade price'], length=7)
    df['1 Month WMA'] = pandas_ta.wma(close=df['Last trade price'], length=30)

    df = signals(df)

    return df




# WMA using ta.trend WMAIndicator
def WMA_ta_trend(content):
    df = content.copy()

    df['1 Day WMA'] = WMAIndicator(close=df['Last trade price'], window=1).wma()
    df['1 Week WMA'] = WMAIndicator(close=df['Last trade price'], window=7).wma()
    df['1 Month WMA'] = WMAIndicator(close=df['Last trade price'], window=30).wma()

    df = signals(df)

    return df



if __name__ == '__main__':
    FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'
    data = pd.read_csv(f"{FOLDER}/KMB.csv")
    data = standardization(data)
    df1 = WMA(data)
    df2 = WMA_ta_trend(data)
    df1.info()
    df2.info()
    print(df1[['1 Day WMA', '1 Week WMA', '1 Month WMA']])
    print(df2[['1 Day WMA', '1 Week WMA', '1 Month WMA']])










# WMA using pandas
def WMA_pandas(content, timeframe):
    df = content[['Date', 'Last trade price']].copy()

    weights = range(1, timeframe + 1)
    df['WMA_pandas'] = df.rolling(timeframe).apply(lambda x: np.dot(x, weights) / sum(weights), raw=True)
    return df

