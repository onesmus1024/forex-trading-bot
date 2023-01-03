import talib as ta
import pandas as pd
from mt5_global import settings
class RisingFallingThreeMethods:
    def __init__(self):
        self.rising_falling_three_methods = 0
    def check_rising_falling_three_methods(self, df)->dict:
        df = pd.DataFrame(df)
        # Raising Falling Three Methods Pattern using talib
        self.rising_falling_three_methods = ta.CDLRISEFALL3METHODS(df['open'], df['high'], df['low'], df['close'])
        self.rising_falling_three_methods = list(self.rising_falling_three_methods)
        if self.rising_falling_three_methods[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'raising_falling_three_methods','sl':settings.sl}
        elif self.rising_falling_three_methods[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'raising_falling_three_methods','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'raising_falling_three_methods not found','sl':0}