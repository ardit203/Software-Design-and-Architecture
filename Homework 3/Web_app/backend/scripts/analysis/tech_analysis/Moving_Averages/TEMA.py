import pandas_ta
import pandas as pd
from backend.scripts.other.standardization import standardization
# SAME

def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'

    df.loc[df['Last trade price'] > df['1 Day TEMA'], '1 Day Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Day TEMA'], '1 Day Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Week TEMA'], '1 Week Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Week TEMA'], '1 Week Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Month TEMA'], '1 Month Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Month TEMA'], '1 Month Signals'] = 'Sell'

    return df



def TEMA(content):
    df = content.copy()
    df['1 Day TEMA'] = pandas_ta.tema(df['Last trade price'], length=1)
    df['1 Week TEMA'] = pandas_ta.tema(df['Last trade price'], length=7)
    df['1 Month TEMA'] = pandas_ta.tema(df['Last trade price'], length=30)

    df = signals(df)
    return df



def TEMA_pandas(content, timeframe):
    df = content[['Date', 'Last trade price']].copy()

    # Step 1: Single EMA
    ema1 = df['Last trade price'].ewm(span=timeframe, adjust=False).mean()

    # Step 2: EMA of EMA (double EMA)
    ema2 = ema1.ewm(span=timeframe, adjust=False).mean()

    # Step 3: EMA of EMA of EMA (triple EMA)
    ema3 = ema2.ewm(span=timeframe, adjust=False).mean()

    # Step 4: Combine to calculate TEMA
    tema = 3 * ema1 - 3 * ema2 + ema3

    df['TEMA_pandas'] = tema

    return df


if __name__ == '__main__':
    FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'
    data = pd.read_csv(f"{FOLDER}/KMB.csv")
    data = standardization(data)
    df = TEMA(data)
    df2 = TEMA_pandas(data,30)
    print(df[['1 Day TEMA', '1 Week TEMA', '1 Month TEMA']])
    print(df2['TEMA_pandas'])




































