import pandas_ta


# The calculation of the oscillators
class Oscillators:

    # Oscillators

    def signals(self, df, kind, buy, sell):
        df[f'1 Day {kind} Signals'] = 'Hold'
        df[f'1 Week {kind} Signals'] = 'Hold'
        df[f'1 Month {kind} Signals'] = 'Hold'
        # Generate signals based on SMA

        df.loc[df[f'1 Day {kind}'] < buy, f'1 Day {kind} Signals'] = 'Buy'
        df.loc[df[f'1 Day {kind}'] > sell, f'1 Day {kind} Signals'] = 'Sell'

        df.loc[df[f'1 Week {kind}'] < buy, f'1 Week {kind} Signals'] = 'Buy'
        df.loc[df[f'1 Week {kind}'] > sell, f'1 Week {kind} Signals'] = 'Sell'

        df.loc[df[f'1 Month {kind}'] < buy, f'1 Month {kind} Signals'] = 'Buy'
        df.loc[df[f'1 Month {kind}'] > sell, f'1 Month {kind} Signals'] = 'Sell'

    def signals_STOCH(self, df):
        df['1 Day STOCH Signals'] = 'Hold'
        df.loc[(df['1 Day STOCH'] > df['%D_1']) & (df['1 Day STOCH'] < 20), '1 Day STOCH Signals'] = 'Buy'  # Buy
        df.loc[(df['1 Day STOCH'] < df['%D_1']) & (df['1 Day STOCH'] > 80), '1 Day STOCH Signals'] = 'Sell'  # Sell

        df['1 Week Signals'] = 'Hold'
        df.loc[(df['1 Week STOCH'] > df['%D_7']) & (df['1 Week STOCH'] < 20), '1 Week STOCH Signals'] = 'Buy'  # Buy
        df.loc[(df['1 Week STOCH'] < df['%D_7']) & (df['1 Week STOCH'] > 80), '1 Week STOCH Signals'] = 'Sell'  # Sell

        df['1 Month Signals'] = 'Hold'
        df.loc[(df['1 Month STOCH'] > df['%D_30']) & (df['1 Month STOCH'] < 20), '1 Month STOCH Signals'] = 'Buy'  # Buy
        df.loc[
            (df['1 Month STOCH'] < df['%D_30']) & (df['1 Month STOCH'] > 80), '1 Month STOCH Signals'] = 'Sell'  # Sell

        df.drop(columns=['%D_1', '%D_7', '%D_30'], inplace=True)

    def RSI(self, df):
        df['1 Day RSI'] = pandas_ta.rsi(close=df['Last trade price'], length=1)
        df['1 Week RSI'] = pandas_ta.rsi(close=df['Last trade price'], length=7)
        df['1 Month RSI'] = pandas_ta.rsi(close=df['Last trade price'], length=30)

    def STOCH_pandas_ta(self, df):
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

    def STOCH(self, df):
        self.calculate_stochastic_oscillator(df, 1, 3, '1 Day STOCH')
        self.calculate_stochastic_oscillator(df, 7, 3, '1 Week STOCH')
        self.calculate_stochastic_oscillator(df, 30, 3, '1 Month STOCH')

    def calculate_stochastic_oscillator(self, df, k_period, d_period, name):
        # Calculate %K
        df['Lowest Low'] = df['Min'].rolling(window=k_period).min()
        df['Highest High'] = df['Max'].rolling(window=k_period).max()
        df[name] = 100 * (df['Last trade price'] - df['Lowest Low']) / (df['Highest High'] - df['Lowest Low'])

        # Calculate %D (SMA of %K)
        df[f'%D_{k_period}'] = df[name].rolling(window=d_period).mean()

        # Clean up intermediate columns
        df.drop(columns=['Lowest Low', 'Highest High'], inplace=True)

    def CCI(self, df):
        df['1 Day CCI'] = pandas_ta.cci(high=df['Max'], low=df['Min'], close=df['Last trade price'], length=1)
        df['1 Week CCI'] = pandas_ta.cci(high=df['Max'], low=df['Min'], close=df['Last trade price'], length=7)
        df['1 Month CCI'] = pandas_ta.cci(high=df['Max'], low=df['Min'], close=df['Last trade price'], length=30)

    def CMO(self, df):
        df['1 Day CMO'] = pandas_ta.cmo(close=df['Last trade price'], length=1)
        df['1 Week CMO'] = pandas_ta.cmo(close=df['Last trade price'], length=7)
        df['1 Month CMO'] = pandas_ta.cmo(close=df['Last trade price'], length=30)

    def WPR(self, df):
        df['1 Day Williams %R'] = pandas_ta.willr(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                                  length=1)

        df['1 Week Williams %R'] = pandas_ta.willr(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                                   length=7)

        df['1 Month Williams %R'] = pandas_ta.willr(high=df['Max'], low=df['Min'], close=df['Last trade price'],
                                                    length=30)
