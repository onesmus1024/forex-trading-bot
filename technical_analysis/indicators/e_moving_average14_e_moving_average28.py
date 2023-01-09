import talib as ta
import pandas as pd
import MetaTrader5 as mt5
from mt5_global import settings


class EMA14_EMA28:
    def __init__(self):
        self.ema14 = 0
        self.ema28 = 0
    def check_ema(self):
        df14 = pd.DataFrame(mt5.copy_rates_from_pos(settings.symbol, settings.timeframe, 1, 14))
        df28 = pd.DataFrame(mt5.copy_rates_from_pos(settings.symbol, settings.timeframe, 1, 20))
        self.ema14 = ta.EMA(df14['close'],timeperiod=14)
        self.ema28 = ta.EMA(df28['close'],timeperiod=20)
        self.ema14 = list(self.ema14)
        self.ema28 = list(self.ema28)
        if self.ema14[-1] > self.ema28[-1]:
            return {'buy':1,'sell':0,'indicator':'ema14_ema28'}
        else:
            return {'buy':0,'sell':1,'indicator':'ema14_ema28'}