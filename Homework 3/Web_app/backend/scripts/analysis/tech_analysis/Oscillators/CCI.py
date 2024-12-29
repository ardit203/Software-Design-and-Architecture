import pandas as pd
import ta.trend as ta
import pandas_ta
# SAME
from backend.scripts.other.standardization import standardization

FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'

def signals(df):

    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'
    # Generate signals based on SMA
    df.loc[df['1 Day CCI'] > 100, '1 Day Signals'] = 'Sell'
    df.loc[df['1 Day CCI'] < -100, '1 Day Signals'] = 'Buy'

    df.loc[df['1 Week CCI'] > 100, '1 Week Signals'] = 'Sell'
    df.loc[df['1 Week CCI'] < -100, '1 Week Signals'] = 'Buy'

    df.loc[df['1 Month CCI'] > 100, '1 Month Signals'] = 'Sell'
    df.loc[df['1 Month CCI'] < -100, '1 Month Signals'] = 'Buy'
    return df


def CCI(content):
    df = content.copy()

    # Calculate CCI using ta library
    df['1 Day CCI'] = ta.cci(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=1,  # Typical period for CCI
        constant=0.015,  # Scaling constant
        fillna=False
    )

    df['1 Week CCI'] = ta.cci(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=7,  # Typical period for CCI
        constant=0.015,  # Scaling constant
        fillna=False
    )

    df['1 Month CCI'] = ta.cci(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=30,  # Typical period for CCI
        constant=0.015,  # Scaling constant
        fillna=False
    )

    df = signals(df)

    return df


def CCI_pandas(content):

    df = content.copy()
    df['1 Day CCI'] = pandas_ta.cci(high=df['Max'], low=df['Min'], close=df['Last trade price'], length=1)
    df['1 Week CCI'] = pandas_ta.cci(high=df['Max'], low=df['Min'], close=df['Last trade price'], length=7)
    df['1 Month CCI'] = pandas_ta.cci(high=df['Max'], low=df['Min'], close=df['Last trade price'], length=30)

    df = signals(df)

    return df

if __name__ == '__main__':
    data = pd.read_csv(f'{FOLDER}/KMB.csv')
    df = standardization(data)

    df1 = CCI_pandas(df)
    df2 = CCI(df)

    print('---TA---')
    print(df2.info())
    print('---PANDAS_TA---')
    print(df1.info())

    # print(df1[['1 Day CCI', '1 Week CCI', '1 Month CCI']])
    # print(df2[['1 Day CCI', '1 Week CCI', '1 Month CCI']])
    # print(df3[['1 Day CCI', '1 Week CCI', '1 Month CCI']])