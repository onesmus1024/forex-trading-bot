import talib as ta
import pandas as pd
from mt5_global import settings
class MorningEveningStar:
    def __init__(self):
        self.morning_star = 0
        self.evening_star = 0
    def check_morning_evening_star(self, df) -> dict:

        """
        Morning and Evening Star Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        df = pd.DataFrame(df)
        self.morning_star = ta.CDLMORNINGSTAR(df['open'], df['high'], df['low'], df['close'])
        self.evening_star = ta.CDLEVENINGSTAR(df['open'], df['high'], df['low'], df['close'])
        self.morning_star = list(self.morning_star)
        self.evening_star = list(self.evening_star)
        if self.morning_star[-1] == 100:
            settings.sl =df['low'].loc[14-3:14].min()
            return {'buy': 1, 'sell':0,'pattern':'morning_star','sl':settings.sl}
        elif self.evening_star[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy': 0, 'sell':1,'pattern':'evening_star','sl':settings.sl}
        else:
            return {'buy': 0, 'sell':0,'pattern':'morning or evening star not found','sl':0}

if __name__ == '__main__':
    #create dummy data for morning star pattern
    import pandas as pd
