import talib as ta
import pandas as pd
from mt5_global import settings

class HammerHangingMan:
    def __init__(self):
        self.hammer = 0
        self.hanging_man = 0
    def check_hammer_hanging_man(self, df) -> dict:
        """
        Morning and Evening Star Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        df = pd.DataFrame(df)
        self.hammer = ta.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
        self.hanging_man = ta.CDLHANGINGMAN(df['open'], df['high'], df['low'], df['close'])
        self.hammer = list(self.hammer)
        self.hanging_man = list(self.hanging_man)
        if self.hammer[-1] == 100:
            settings.sl =df['low'].loc[14-3:14].min()
            return {'buy': 1, 'sell':0,'pattern':'hammer','sl':settings.sl}
        elif self.hanging_man[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy': 0, 'sell':1,'pattern':'hanging man ','sl':settings.sl}
        else:
            return {'buy': 0, 'sell':0,'pattern':'hammer or hanging man not found','sl':0}