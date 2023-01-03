import talib as ta
import pandas as pd
from mt5_global import settings
class Unique3River:
    def __init__(self):
        self.unique_three_river = 0
    def check_unique_three_river(self, df)->dict:
        df = pd.DataFrame(df)
        self.unique_three_river = ta.CDL3INSIDE(df['open'], df['high'], df['low'], df['close'])
        self.unique_three_river = list(self.unique_three_river)
        if self.unique_three_river[-1] == 100:
            settings.sl = df['low'].min()
            return {'buy':1,'sell':0,'pattern':'unique_three_river','sl':settings.sl}
        elif self.unique_three_river[-1] == -100:
            settings.sl = df['high'].max()
            return {'buy':0,'sell':1,'pattern':'unique_three_river','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'unique_three_river not found','sl':0}