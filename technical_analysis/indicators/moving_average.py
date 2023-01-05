import talib as ta
import pandas as pd

class MovingAverage:
    def __init__(self):
        self.ma = 0
    def check_ma(self,df):
        df = pd.DataFrame(df)
        

        self.ma = ta.SMA(df['close'],timeperiod=14)
        self.ma = list(self.ma)
        close =list(df['close'])
        if self.ma[-1] < close[-1]:
            return {'buy':1,'sell':0,'indicator':'sma'}
        else:
            return {'buy':0,'sell':1,'indicator':'sma'}


