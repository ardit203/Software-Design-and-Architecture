import pandas as pd
from datetime import datetime
from backend.scripts.other.standardization import standardization, de_standardization

from backend.scripts.analysis.tech_analysis.Moving_Averages import TEMA, EMA, HMA, SMA, WMA

from backend.scripts.analysis.tech_analysis.Oscillators import CCI, STOCH, RSI, CMO, WPR

# Moving Averages (SMA, EMA, WMA, HMA, TEMA)

# Oscillators (RSI, STOCH, CCI, Williams %R, CMO)

dict = {
    '1Day': 1,
    '1Week': 7,
    '1Month': 30
}

FOLDER = 'D:/Faculty/5th Semester/PYTHON/backend/database'

def tech_main(issuer: str, indicator: str, from_date):
    data = pd.read_csv(f'{FOLDER}/{issuer}.csv')
    df = data[['Date', 'Last trade price', 'Max', 'Min']].copy()
    df = standardization(df)

    copy = None


    if indicator == 'SMA':
        copy = SMA.SMA(df)

    if indicator == 'EMA':
        copy = EMA.EMA(df)

    if indicator == 'WMA':
        copy = WMA.WMA(df)

    if indicator == 'HMA':
        copy = HMA.HMA(df)

    if indicator == 'TEMA':
        copy = TEMA.TEMA(df)

    if indicator == 'RSI':
        copy = RSI.RSI(df)

    if indicator == 'STOCH':
        copy = STOCH.STOCH(df)

    if indicator == 'CCI':
        copy = CCI.CCI(df)

    if indicator == 'Williams %R':
        copy = WPR.WPR(df)

    if indicator == 'CMO':
        copy = CMO.CMO(df)



    if from_date is not None:
        copy = copy[copy['Date'] >= from_date]
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        if from_date < copy['Date'].min():
            from_date = copy['Date'].min()

    de_standardization(copy)
    if len(copy):
        return copy

    return "Not good"



# total TURNOVER = Avg.Prive * Volume

#