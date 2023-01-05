import talib as ta
import pandas as pd
from mt5_global import settings

class RelativeStrengthIndex:
    def __init__(self):
        self.rsi = 0
    def check_rsi(self,df):
        df = pd.DataFrame(df)
        self.rsi = ta.RSI(df['close'],timeperiod=14)
        self.rsi = list(self.rsi)
        close =list(df['close'])
        if self.rsi[-1] < 30:
            return {'buy':1,'sell':0,'indicator':'rsi'}
        elif self.rsi[-1] > 70:
            return {'buy':0,'sell':1,'indicator':'rsi'}
        else:
            return {'buy':0,'sell':0,'indicator':'rsi'}
        #check for divergence
