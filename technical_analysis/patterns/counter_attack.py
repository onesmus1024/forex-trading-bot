import talib as ta
from mt5_global import settings
class CounterAttack:
    def __init__(self):
        self.counter_attack = 0
    def check_counter_attack(self, df)->dict:
        # Counter Attack Pattern using talib
        self.counter_attack = ta.CDLCOUNTERATTACK(df['open'], df['high'], df['low'], df['close'])
        self.counter_attack = list(self.counter_attack)
        if self.counter_attack[-1] == 100:
            settings.sl = df['low'].loc[14-3:14].min()
            return {'buy':1,'sell':0,'pattern':'counter_attack','sl':settings.sl}
        elif self.counter_attack[-1] == -100:
            settings.sl = df['high'].loc[14-3:14].max()
            return {'buy':0,'sell':1,'pattern':'counter_attack','sl':settings.sl}
        else:
            return {'buy':0,'sell':0,'pattern':'counter_attack not found','sl':0}