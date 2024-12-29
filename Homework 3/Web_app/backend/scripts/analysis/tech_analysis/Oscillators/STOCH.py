import pandas as pd
from ta.momentum import stoch, stoch_signal
import pandas_ta

from backend.scripts.other.standardization import standardization

FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'


def signals(df):
    df['1 Day Signals'] = 'Hold'
    df.loc[(df['1 Day STOCH'] > df['%D_1']) & (df['1 Day STOCH'] < 20), '1 Day Signals'] = 'Buy'  # Buy
    df.loc[(df['1 Day STOCH'] < df['%D_1']) & (df['1 Day STOCH'] > 80), '1 Day Signals'] = 'Sell'  # Sell

    df['1 Week Signals'] = 'Hold'
    df.loc[(df['1 Week STOCH'] > df['%D_7']) & (df['1 Week STOCH'] < 20), '1 Week Signals'] = 'Buy'  # Buy
    df.loc[(df['1 Week STOCH'] < df['%D_7']) & (df['1 Week STOCH'] > 80), '1 Week Signals'] = 'Sell'  # Sell

    df['1 Month Signals'] = 'Hold'
    df.loc[(df['1 Month STOCH'] > df['%D_30']) & (df['1 Month STOCH'] < 20), '1 Month Signals'] = 'Buy'  # Buy
    df.loc[(df['1 Month STOCH'] < df['%D_30']) & (df['1 Month STOCH'] > 80), '1 Month Signals'] = 'Sell'  # Sell

    # # Generate Buy/Sell signals based on the Stochastic Oscillator
    # df['Buy Signal'] = (df['%K'] > df['%D']) & (df['%K'].shift(1) <= df['%D'].shift(1))  # Bullish crossover
    # df['Sell Signal'] = (df['%K'] < df['%D']) & (df['%K'].shift(1) >= df['%D'].shift(1))  # Bearish crossover

    return df


def STOCH(content):
    df = content.copy()

    # Calculate Stochastic Oscillator (%K and %D)
    stoch1 = pandas_ta.stoch(high=df['Max'], low=df['Min'], close=df['Last trade price'], k=1, smooth_k=3, d=3)
    stoch7 = pandas_ta.stoch(high=df['Max'], low=df['Min'], close=df['Last trade price'], k=7, smooth_k=3, d=3)
    stoch30 = pandas_ta.stoch(high=df['Max'], low=df['Min'], close=df['Last trade price'], k=30, smooth_k=3, d=3)

    # Add the %K and %D columns to the DataFrame
    df['1 Day STOCH'] = stoch1['STOCHk_1_3_3']  # %K line
    df['%D_1'] = stoch1['STOCHd_1_3_3']  # %D line (signal line)

    df['1 Week STOCH'] = stoch7['STOCHk_7_3_3']  # %K line
    df['%D_7'] = stoch7['STOCHd_7_3_3']  # %D line (signal line)

    df['1 Month STOCH'] = stoch30['STOCHk_30_3_3']  # %K line
    df['%D_30'] = stoch30['STOCHd_30_3_3']  # %D line (signal line)

    df = signals(df)
    return df


def STOCH_ta(content):
    df = content.copy()

    # Calculate Stochastic Oscillator
    df['1 Day STOCH'] = stoch(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=1,  # %K period
        smooth_window=3,  # %D smoothing period
        fillna=False
    )

    df['%D_1'] = stoch_signal(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=1,
        smooth_window=3,
        fillna=False
    )

    ##############################################################################

    df['1 Week STOCH'] = stoch(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=7,  # %K period
        smooth_window=3,  # %D smoothing period
        fillna=False
    )

    df['%D_7'] = stoch_signal(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=7,
        smooth_window=3,
        fillna=False
    )

    ##################################################################################################################

    df['1 Month STOCH'] = stoch(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=30,  # %K period
        smooth_window=3,  # %D smoothing period
        fillna=False
    )

    df['%D_30'] = stoch_signal(
        high=df['Max'],
        low=df['Min'],
        close=df['Last trade price'],
        window=30,
        smooth_window=3,
        fillna=False
    )

    df = signals(df)
    return df


def calculate_stochastic_oscillator(content, k_period, d_period):
    df = content.copy()

    # Calculate %K
    df['Lowest Low'] = df['Min'].rolling(window=k_period).min()
    df['Highest High'] = df['Max'].rolling(window=k_period).max()
    df['STOCH'] = 100 * (df['Last trade price'] - df['Lowest Low']) / (df['Highest High'] - df['Lowest Low'])

    # Calculate %D (SMA of %K)
    df['%D'] = df['STOCH'].rolling(window=d_period).mean()

    # Clean up intermediate columns
    df.drop(columns=['Lowest Low', 'Highest High'], inplace=True)

    df = signals(df)

    return df


if __name__ == '__main__':
    data = pd.read_csv(f'{FOLDER}/KMB.csv')
    df = standardization(data)
    st = STOCH(df)
    st2 = STOCH_ta(df)

    print('---TA---')
    print(st2.info())
    print('---PANDAS_TA---')
    print(st.info())

    # print(st[['1 Day STOCH', '1 Week STOCH', '1 Month STOCH']])
    # print(st2[['1 Day STOCH', '1 Week STOCH', '1 Month STOCH']])
