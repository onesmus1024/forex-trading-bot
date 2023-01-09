import talib as ta
import pandas as pd

class StochasticOscillator:
    def __init__(self):
        self.slowk = 0
        self.slowd = 0
    def check_stoch(self,df):
        df = pd.DataFrame(df)
        self.slowk,self.slowd = ta.STOCH(df['high'],df['low'],df['close'],fastk_period=14,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)
        self.slowk = list(self.slowk)
        self.slowd = list(self.slowd)
        if self.slowk[-1] > self.slowd[-1]:
            return {'buy':1,'sell':0,'indicator':'stoch'}
        elif self.slowk[-1] < self.slowd[-1]:
            return {'buy':0,'sell':1,'indicator':'stoch'}
        else:
            return {'buy':0,'sell':0,'indicator':'stoch'}