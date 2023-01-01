import talib as ta
from mt5_global import settings

class ShootingStartInvertedHammer:
    def __init__(self):
        self.shooting_star = 0
        self.inverted_hammer = 0
    def check_shooting_start_inverted_hammer(self, df) -> dict:
        """
        Morning and Evening Star Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        self.shooting_star = ta.CDLSHOOTINGSTAR(df['open'], df['high'], df['low'], df['close'])
        self.inverted_hammer = ta.CDLINVERTEDHAMMER(df['open'], df['high'], df['low'], df['close'])
        self.shooting_star = list(self.shooting_star)
        self.inverted_hammer = list(self.inverted_hammer)
        if self.shooting_star[-1] == 100:
            settings.sl =df['low'].loc[14-3:14].min()
            return {'buy': 1, 'sell':0,'pattern':'shooting_star','sl':settings.sl}
        elif self.inverted_hammer[-1] == 100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy': 0, 'sell':1,'pattern':'inverted_hammer','sl':settings.sl}
        else:
            return {'buy': 0, 'sell':0,'pattern':'shooting star or inverted hammer not found','sl':0}