import time
from Database.Database import Database
from Scripts.Technical.MovingAverages import MovingAverages
from Scripts.Technical.Oscillators import Oscillators

# Used to make the technical analysis and save the data to the database
class Technical:
    _db = Database()
    _ma = MovingAverages()
    _osc = Oscillators()

    # Moving Averages
    def _SMA(self, df):
        self._ma.SMA(df)
        self._ma.signals(df, 'SMA')

    def _EMA(self, df):
        self._ma.EMA(df)
        self._ma.signals(df, 'EMA')

    def _WMA(self, df):
        self._ma.WMA(df)
        self._ma.signals(df, 'WMA')

    def _HMA(self, df):
        self._ma.HMA(df)
        self._ma.signals(df, 'HMA')

    def _TEMA(self, df):
        self._ma.TEMA(df)
        self._ma.signals(df, 'TEMA')

    # Oscillators

    def _RSI(self, df):
        self._osc.RSI(df)
        self._osc.signals(df, 'RSI', 20, 80)

    def _STOCH(self, df):
        self._osc.STOCH(df)
        self._osc.signals_STOCH(df)

    def _CCI(self, df):
        self._osc.CCI(df)
        self._osc.signals(df, 'CCI', -100, 100)

    def _CMO(self, df):
        self._osc.CMO(df)
        self._osc.signals(df, 'CMO', 0, 0)

    def _WPR(self, df):
        self._osc.WPR(df)
        self._osc.signals(df, 'Williams %R', -80, -20)

    def _tech_implementation(self, issuers):

        for issuer in issuers:
            data = self._db.read(issuer, 'std')
            if data is None:
                continue

            data = data[['Date', 'Last trade price', 'Max', 'Min']]
            data['Max'] = data['Max'].fillna(data['Last trade price'])
            data['Min'] = data['Min'].fillna(data['Last trade price'])

            self._SMA(data)
            self._EMA(data)
            self._HMA(data)
            self._WMA(data)
            self._TEMA(data)
            self._RSI(data)
            self._STOCH(data)
            self._CCI(data)
            self._CMO(data)
            self._WPR(data)
            self._db.save(issuer, 'technical', data)

    def start(self):
        print("STARTED THE TECHNICAL ANALYSIS")
        start_t = time.time()
        issuers = self._db.read('Issuers', 'stock')['Code'].values.tolist()
        self._tech_implementation(issuers)
        print('TIME TAKEN TO MAKE TECH ANALYSIS: ', round((time.time() - start_t) / 60, 2), 'min  or ',
              round(time.time() - start_t, 2), 'sec')


if __name__ == '__main__':
    tech = Technical()
    tech.start()
