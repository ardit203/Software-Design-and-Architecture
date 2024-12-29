import pandas as pd
import pandas_ta
import numpy as np
# SAME NOT SAME FOR 1
from backend.scripts.other.standardization import standardization


def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'

    df.loc[df['Last trade price'] > df['1 Day HMA'], '1 Day Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Day HMA'], '1 Day Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Week HMA'], '1 Week Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Week HMA'], '1 Week Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Month HMA'], '1 Month Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Month HMA'], '1 Month Signals'] = 'Sell'

    return df


# HMA using pandas_ta.hma
def HMA(content):
    df = content.copy()

    df['1 Day HMA'] = pandas_ta.hma(df['Last trade price'], length=1)
    df['1 Week HMA'] = pandas_ta.hma(df['Last trade price'], length=7)
    df['1 Month HMA'] = pandas_ta.hma(df['Last trade price'], length=30)
    # df['HMA'] = df['Price'].ta.hma(length=timeframe)

    df = signals(df)
    return df



# HMA using pandas
def HMA_pandas(content, timeframe):
    df = content[['Date', 'Last trade price']].copy()

    def WMA_pandas(cnt, window):
        weights = range(1, window + 1)
        return cnt.rolling(window).apply(lambda x: np.dot(x, weights) / sum(weights), raw=True)

    half_period = int(timeframe / 2)
    wma_half = WMA_pandas(df['Last trade price'], half_period)

    # Step 2: WMA of full period
    wma_full = WMA_pandas(df['Last trade price'], timeframe)

    # Step 3: Adjusted WMA
    adjusted_wma = 2 * wma_half - wma_full

    # Step 4: Final WMA using sqrt(period)
    sqrt_period = int(np.sqrt(timeframe))
    hma_series = WMA_pandas(adjusted_wma, sqrt_period)

    df['HMA_pandas'] = hma_series
    return df


if __name__ == '__main__':
    FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'
    data = pd.read_csv(f"{FOLDER}/KMB.csv")
    data = standardization(data)
    df = HMA(data)
    df2 = HMA_pandas(data,30)
    print(df[['1 Day HMA', '1 Week HMA', '1 Month HMA']])
    print(df2['HMA_pandas'])



















