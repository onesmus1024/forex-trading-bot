import talib as ta
import pandas as pd
from mt5_global import settings
class ThreeBlackCrowsThreeAdvancingSolders:
    def __init__(self):
        self.three_black_crows = 0
        self.three_advancing_solders = 0
        self.advancing_block = 0
        self.stalled_pattern = 0

    def check_three_black_crows_three_advancing_solders(self, df)->dict:
        df = pd.DataFrame(df)
        # Three Black Crows Pattern using talib
        self.three_black_crows = ta.CDL3BLACKCROWS(df['open'], df['high'], df['low'], df['close'])
        self.three_advancing_solders = ta.CDL3WHITESOLDIERS(df['open'], df['high'], df['low'], df['close'])
        self.advancing_block = ta.CDLADVANCEBLOCK(df['open'], df['high'], df['low'], df['close'])
        self.stalled_pattern = ta.CDLSTALLEDPATTERN(df['open'], df['high'], df['low'], df['close'])
        self.three_black_crows = list(self.three_black_crows)
        self.three_advancing_solders = list(self.three_advancing_solders)
        self.advancing_block = list(self.advancing_block)
        self.stalled_pattern = list(self.stalled_pattern)
        if self.three_black_crows[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'three_black_crows','sl':settings.sl}
        elif self.three_advancing_solders[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'three_advancing_solders','sl':settings.sl}
        elif self.advancing_block[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'advancing_block','sl':settings.sl}
        elif self.stalled_pattern[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'stalled_pattern','sl':settings.sl}
        elif self.advancing_block[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'advancing_block','sl':settings.sl}
        elif self.stalled_pattern[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'stalled_pattern','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':' three_black_crows_three_advancing_solders not found','sl':0}