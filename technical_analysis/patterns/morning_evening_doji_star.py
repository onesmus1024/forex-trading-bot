import talib as ta
import pandas as pd
from mt5_global import settings
class MorningEveningDoji:
    def __init__(self):
        self.morning_doji_star = 0
        self.evening_doji_star = 0
    def check_moring_evining_doji(self, df) -> dict:
        """
        Morning and Evening Star Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        df = pd.DataFrame(df)
        self.morning_doji_star = ta.CDLMORNINGDOJISTAR(df['open'], df['high'], df['low'], df['close'], penetration=0)
        self.evening_doji_star = ta.CDLEVENINGDOJISTAR(df['open'], df['high'], df['low'], df['close'], penetration=0)
        self.morning_doji_star = list(self.morning_doji_star)
        self.evening_doji_star = list(self.evening_doji_star)
        if self.morning_doji_star[-1] == 100:
            settings.sl =df['low'].loc[14-3:14].min()
            return {'buy': 1, 'sell':0,'pattern':'morning_doji_star','sl':settings.sl}
        elif self.evening_doji_star[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy': 0, 'sell':1,'pattern':'evening_doji_star','sl':settings.sl}
        else:
            return {'buy': 0, 'sell':0,'pattern':'morning or evening doji star not found','sl':0}
