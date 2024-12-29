import pandas as pd
import pandas_ta
from backend.scripts.other.standardization import standardization


def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'

    df.loc[df['1 Day CMO'] > 0, '1 Day Signals'] = 'Buy'
    df.loc[df['1 Day CMO'] < 0, '1 Day Signals'] = 'Sell'

    df.loc[df['1 Week CMO'] > 0, '1 Week Signals'] = 'Buy'
    df.loc[df['1 Week CMO'] < 0, '1 Week Signals'] = 'Sell'

    df.loc[df['1 Month CMO'] > 0, '1 Month Signals'] = 'Buy'
    df.loc[df['1 Month CMO'] < 0, '1 Month Signals'] = 'Sell'

    return df

def CMO(content):
    df = content.copy()


    df['1 Day CMO'] = pandas_ta.cmo(close=df['Last trade price'], length=1)
    df['1 Week CMO'] = pandas_ta.cmo(close=df['Last trade price'], length=7)
    df['1 Month CMO'] = pandas_ta.cmo(close=df['Last trade price'], length=30)

    # df = signals(df)

    return df



def CMO_panda(content):
    df = content.copy()
    # Define the lookback period
    period = 14

    # Calculate price changes
    df['Change'] = df['Close'].diff()

    # Separate gains and losses
    df['Gain'] = df['Change'].where(df['Change'] > 0, 0)
    df['Loss'] = -df['Change'].where(df['Change'] < 0, 0)

    # Calculate sum of gains and losses over the period
    df['Sum of Gains'] = df['Gain'].rolling(window=period).sum()
    df['Sum of Losses'] = df['Loss'].rolling(window=period).sum()

    # Calculate CMO
    df['CMO'] = ((df['Sum of Gains'] - df['Sum of Losses']) /
                 (df['Sum of Gains'] + df['Sum of Losses'])) * 100



FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'

if __name__ == '__main__':
    data = pd.read_csv(f'{FOLDER}/KMB.csv')
    data = standardization(data)
    df1 = CMO(data)
    df1.info()
    # df2 = WPR_ta(data)
    # print(df1[['1 Day CMO', '1 Week CMO', '1 Month CMO']])
    # print(df2[['1 Day Williams %R', '1 Week Williams %R', '1 Month Williams %R']])