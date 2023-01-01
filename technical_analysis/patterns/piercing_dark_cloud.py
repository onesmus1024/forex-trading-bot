import talib as ta
from mt5_global import settings
class PiercingDarkCloud:
    def __init__(self):
        self.piercing = 0
        self.dark_cloud = 0
    def check_piercing_dark_cloud(self, df) -> dict:
        """
        Morning and Evening Star Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        self.piercing = ta.CDLPIERCING(df['open'], df['high'], df['low'], df['close'])
        self.dark_cloud = ta.CDLDARKCLOUDCOVER(df['open'], df['high'], df['low'], df['close'], penetration=0)
        self.piercing = list(self.piercing)
        self.dark_cloud = list(self.dark_cloud)
        if self.piercing[-1] == 100:
            settings.sl =df['low'].loc[14-3:14].min()
            return {'buy': 1, 'sell':0,'pattern':'piercing','sl':settings.sl}
        elif self.dark_cloud[-1] == 100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy': 0, 'sell':1,'pattern':'dark_cloud','sl':settings.sl}
        else:
            return {'buy': 0, 'sell':0,'pattern':'piercing or dark cloud not found','sl':0}