from .patterns.bearish_bullish import BearishBullishEnglufing
from .patterns.morning_evening_star import MorningEveningStar
from .patterns.piercing_dark_cloud import PiercingDarkCloud
from .patterns.morning_evening_doji_star import MorningEveningDoji
from mt5_actions import rates
from mt5_global.settings import timeframe,symbol

class Signal(BearishBullishEnglufing, MorningEveningStar, PiercingDarkCloud, MorningEveningDoji):
    def __init__(self):
        self.signal =[]

    def get_signal(self):
        self.signal.append(self.check_bearish_bullish(rates.get_curr_rates(symbol,timeframe,1)))
        self.signal.append(self.check_morning_evening_star(rates.get_curr_rates(symbol,timeframe,1)))
        self.signal.append(self.check_piercing_Dark_cloud(rates.get_curr_rates(symbol,timeframe,1)))
        self.signal.append(self.check_morning_evening_doji(rates.get_curr_rates(symbol,timeframe,1)))
        return self.signal

    #function to check signal type either buy or sell by checking the signal list which contains {'buy':0, 'sell':0}
    def check_signal_type(self):
        sell = 0
        buy = 0
        signal_type = ''
        for signal in self.signal:
            if signal['buy'] == 1:
                buy += 1
            elif signal['sell'] == 1:
                sell += 1
        if buy > sell and sell==0:
            signal_type = 'buy'
        elif sell > buy and buy==0:
            signal_type = 'sell'
        else:
            signal_type = 'hold'
        return signal_type

if __name__ == "__main__":
    signal = Signal()
    print(signal.get_signal())
    print(signal.check_signal_type())