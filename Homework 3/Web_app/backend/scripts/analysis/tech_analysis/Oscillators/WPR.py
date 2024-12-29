import pandas as pd
import pandas_ta
from ta.momentum import WilliamsRIndicator
# SAME
from backend.scripts.other.standardization import standardization


def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'


    df.loc[df['1 Day Williams %R'] < -80, '1 Day Signals'] = 'Buy'
    df.loc[df['1 Day Williams %R'] > -20, '1 Day Signals'] = 'Sell'

    df.loc[df['1 Week Williams %R'] < -80, '1 Week Signals'] = 'Buy'
    df.loc[df['1 Week Williams %R'] > -20, '1 Week Signals'] = 'Sell'

    df.loc[df['1 Month Williams %R'] < -80, '1 Month Signals'] = 'Buy'
    df.loc[df['1 Month Williams %R'] > -20, '1 Month Signals'] = 'Sell'

    return df

def fill(df):
    df['1 Day Williams %R'] = df['1 Day Williams %R'].fillna(df['1 Day Williams %R'].mean())

    df['1 Week Williams %R'] = df['1 Week Williams %R'].fillna(df['1 Week Williams %R'].mean())

    df['1 Month Williams %R'] = df['1 Month Williams %R'].fillna(df['1 Month Williams %R'].mean())

def WPR(content):
    df = content.copy()

    df['1 Day Williams %R'] = pandas_ta.willr(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                              length=1)

    df['1 Week Williams %R'] = pandas_ta.willr(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                              length=7)

    df['1 Month Williams %R'] = pandas_ta.willr(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                              length=30)

    # fill(df)
    df = signals(df)

    return df

def WPR_ta(content):
    df = content.copy()

    df['1 Day Williams %R'] = WilliamsRIndicator(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                                 lbp=1).williams_r()

    df['1 Week Williams %R'] = WilliamsRIndicator(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                                  lbp=7).williams_r()

    df['1 Month Williams %R'] = WilliamsRIndicator(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                                   lbp=30).williams_r()

    df = signals(df)

    return df



FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'

if __name__ == '__main__':
    data = pd.read_csv(f'{FOLDER}/KMB.csv')
    data = standardization(data)
    df1 = WPR(data)
    df2 = WPR_ta(data)

    print('---TA---')
    print(df2.info())
    print('---PANDAS_TA---')
    print(df1.info())
