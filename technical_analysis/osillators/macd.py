import talib as ta
import pandas as pd
from mt5_global import settings

class MACD:
    def __init__(self):
        self.macd = 0
        self.macdsignal = 0
        self.macdhist = 0
    def check_macd(self,df):
        df = pd.DataFrame(df)
        self.macd,self.macdsignal,self.macdhist = ta.MACD(df['close'],fastperiod=12,slowperiod=26,signalperiod=9)
        self.macd = list(self.macd)
        self.macdsignal = list(self.macdsignal)
        self.macdhist = list(self.macdhist)
        if self.macdhist[-1] > self.macdhist[-2]:
            return {'buy':1,'sell':0,'indicator':'macd'}
        elif self.macdhist[-1] < self.macdhist[-2]:
            return {'buy':0,'sell':1,'indicator':'macd'}
        else:
            return {'buy':0,'sell':0,'indicator':'macd'}