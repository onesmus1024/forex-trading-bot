import talib as ta
import pandas as pd
from mt5_global import settings
class TasukiGap:
    def __init__(self):
        self.tasuki_gap = 0
    def check_tasuki_gap(self, df)->dict:
        df = pd.DataFrame(df)
        # Tasuki Gap Pattern using talib
        self.tasuki_gap = ta.CDLTASUKIGAP(df['open'], df['high'], df['low'], df['close'])
        self.tasuki_gap = list(self.tasuki_gap)
        if self.tasuki_gap[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'tasuki_gap','sl':settings.sl}
        elif self.tasuki_gap[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'tasuki_gap','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'tasuki_gap not found','sl':0}