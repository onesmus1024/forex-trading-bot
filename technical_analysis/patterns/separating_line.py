import talib as ta
import pandas as pd
from mt5_global import settings
class SeparatingLine:
    def __init__(self):
        self.separating_line = 0
    def check_separating_line(self, df)->dict:
        df = pd.DataFrame(df)
        # Separating Line Pattern using talib
        self.separating_line = ta.CDLSEPARATINGLINES(df['open'], df['high'], df['low'], df['close'])
        self.separating_line = list(self.separating_line)
        if self.separating_line[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'separating_line','sl':settings.sl}
        elif self.separating_line[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'separating_line','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'separating_line not found','sl':0}