import talib as ta
from mt5_global import settings
class Harami:
    def __init__(self):
        self.harami = 0
        self.harami_cross = 0

    def check_harami(self, df)->dict:
        # Harami Pattern using talib
        self.harami = ta.CDLHARAMI(df['open'], df['high'], df['low'], df['close'])
        self.harami_cross = ta.CDLHARAMICROSS(df['open'], df['high'], df['low'], df['close'])
        self.harami = list(self.harami)
        self.harami_cross = list(self.harami_cross)
        if self.harami[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'harami','sl':settings.sl}
        elif self.harami_cross[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'harami_cross','sl':settings.sl}
        elif self.harami[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'harami','sl':settings.sl}
        elif self.harami_cross[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'harami_cross','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'harami or harami_cross not found','sl':0}