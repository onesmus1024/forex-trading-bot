import talib as ta
from mt5_global import settings
class Doji:
    def __init__(self):
        self.doji = 0
    def check_doji(self, df)->dict:
        # Doji Pattern using talib
        self.doji = ta.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
        self.doji = list(self.doji)
        if self.doji[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'doji','sl':settings.sl}
        elif self.doji[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'doji','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'doji not found','sl':0}