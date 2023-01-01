import talib as ta
from mt5_global import settings
class UpsideGap2Crows:
    def __init__(self):
        self.upside_gap_2_crows = 0
    def check_upside_gap_2_crows(self, df)->dict:
        self.upside_gap_2_crows = ta.CDLXSIDEGAP3METHODS(df['open'], df['high'], df['low'], df['close'])
        self.upside_gap_2_crows = list(self.upside_gap_2_crows)
        if self.upside_gap_2_crows[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'upside_gap_2_crows','sl':settings.sl}
        elif self.upside_gap_2_crows[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'upside_gap_2_crows','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'upside_gap_2_crows not found','sl':0}