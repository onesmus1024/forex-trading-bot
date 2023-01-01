import time
import talib as ta
from mt5_global import settings
class BearishBullishEnglufing:
    def __init__(self):
        self.bullish_engulfing = 0
        self.bearish_engulfing = 0
    def check_bullish_bearish_engulfing(self, df)->dict:
        # Bullish Engulfing Pattern using talib
        self.bullish_engulfing = ta.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
        self.bearish_engulfing = ta.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
        self.bullish_engulfing = list(self.bullish_engulfing)
        self.bearish_engulfing = list(self.bearish_engulfing)
        if self.bullish_engulfing[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'bullish_engulfing','sl':settings.sl}
        elif self.bearish_engulfing[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'bearish_engulfing','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'bearish or bullish engulfing not found','sl':0}