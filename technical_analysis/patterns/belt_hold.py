import talib as ta
import pandas as pd
from mt5_global import settings
class BeltHold:
    def __init__(self):
        self.belt_hold = 0
    def check_belt_hold(self, df)->dict:
        df = pd.DataFrame(df)
        # Belt Hold Pattern using talib
        self.belt_hold = ta.CDLBELTHOLD(df['open'], df['high'], df['low'], df['close'])
        self.belt_hold = list(self.belt_hold)
        if self.belt_hold[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'belt_hold','sl':settings.sl}
        elif self.belt_hold[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'belt_hold','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'belt_hold not found','sl':0}