import pandas_ta

# The calculation of the moving averages
class MovingAverages:

    # Moving Averages

    def signals(self, df, kind):

        df[f'1 Day {kind} Signals'] = 'Hold'
        df[f'1 Week {kind} Signals'] = 'Hold'
        df[f'1 Month {kind} Signals'] = 'Hold'

        df.loc[df['Last trade price'] > df[f'1 Day {kind}'], f'1 Day {kind} Signals'] = 'Buy'
        df.loc[df['Last trade price'] < df[f'1 Day {kind}'], f'1 Day {kind} Signals'] = 'Sell'

        df.loc[df['Last trade price'] > df[f'1 Week {kind}'], f'1 Week {kind} Signals'] = 'Buy'
        df.loc[df['Last trade price'] < df[f'1 Week {kind}'], f'1 Week {kind} Signals'] = 'Sell'

        df.loc[df['Last trade price'] > df[f'1 Month {kind}'], f'1 Month {kind} Signals'] = 'Buy'
        df.loc[df['Last trade price'] < df[f'1 Month {kind}'], f'1 Month {kind} Signals'] = 'Sell'

    def SMA(self, df):
        df['1 Day SMA'] = df['Last trade price'].rolling(window=1).mean()
        df['1 Week SMA'] = df['Last trade price'].rolling(window=7).mean()
        df['1 Month SMA'] = df['Last trade price'].rolling(window=30).mean()


    def EMA(self, df):
        df['1 Day EMA'] = df['Last trade price'].ewm(span=1, adjust=False).mean()
        df['1 Week EMA'] = df['Last trade price'].ewm(span=7, adjust=False).mean()
        df['1 Month EMA'] = df['Last trade price'].ewm(span=30, adjust=False).mean()


    def WMA(self, df):
        df['1 Day WMA'] = pandas_ta.wma(close=df['Last trade price'], length=1)
        df['1 Week WMA'] = pandas_ta.wma(close=df['Last trade price'], length=7)
        df['1 Month WMA'] = pandas_ta.wma(close=df['Last trade price'], length=30)


    def HMA(self, df):
        df['1 Day HMA'] = pandas_ta.hma(df['Last trade price'], length=1)
        df['1 Week HMA'] = pandas_ta.hma(df['Last trade price'], length=7)
        df['1 Month HMA'] = pandas_ta.hma(df['Last trade price'], length=30)


    def TEMA(self, df):
        df['1 Day TEMA'] = pandas_ta.tema(df['Last trade price'], length=1)
        df['1 Week TEMA'] = pandas_ta.tema(df['Last trade price'], length=7)
        df['1 Month TEMA'] = pandas_ta.tema(df['Last trade price'], length=30)

