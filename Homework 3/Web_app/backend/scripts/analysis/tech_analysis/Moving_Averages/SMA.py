import pandas as pd

from backend.scripts.other.standardization import standardization


def signals(df):
    df['1 Day Signals'] = 'Hold'
    df['1 Week Signals'] = 'Hold'
    df['1 Month Signals'] = 'Hold'

    df.loc[df['Last trade price'] > df['1 Day SMA'], '1 Day Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Day SMA'], '1 Day Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Week SMA'], '1 Week Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Week SMA'], '1 Week Signals'] = 'Sell'

    df.loc[df['Last trade price'] > df['1 Month SMA'], '1 Month Signals'] = 'Buy'
    df.loc[df['Last trade price'] < df['1 Month SMA'], '1 Month Signals'] = 'Sell'

    return df


def SMA(content: pd.DataFrame):
    df = content.copy()

    df['1 Day SMA'] = df['Last trade price'].rolling(window=1).mean()
    df['1 Week SMA'] = df['Last trade price'].rolling(window=7).mean()
    df['1 Month SMA'] = df['Last trade price'].rolling(window=30).mean()

    df = signals(df)

    return df



if __name__ == '__main__':
    FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'
    data = pd.read_csv(f"{FOLDER}/KMB.csv")
    data = standardization(data)
    df = SMA(data)
    df.info()
    print(df[['1 Day SMA', '1 Week SMA', '1 Month SMA']].head(40))



# data['SMA_10'] = data['Close'].rolling(window=10).mean()
#
# # Calculate the slope of the SMA
# data['SMA_10_Change'] = data['SMA_10'].diff()
#
# # Generate Buy/Sell signals
# data['Signal'] = 0
# data.loc[data['SMA_10_Change'] > 0, 'Signal'] = 1  # Buy
# data.loc[data['SMA_10_Change'] < 0, 'Signal'] = -1  # Sell
