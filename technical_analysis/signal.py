from .patterns.bearish_bullish_engulfing import BearishBullishEnglufing
from .patterns.morning_evening_star import MorningEveningStar
from .patterns.piercing_dark_cloud import PiercingDarkCloud
from .patterns.morning_evening_doji_star import MorningEveningDoji
from .patterns.hammer_hanging_man import HammerHangingMan
from .patterns.shooting_start_inverted_hammer import ShootingStartInvertedHammer
from .patterns.harami import Harami
from .patterns.belt_hold import BeltHold
from .patterns.doji import Doji
from .patterns.threeblackcrows_threeadvancingsolders import ThreeBlackCrowsThreeAdvancingSolders
from .patterns.unique3river import Unique3River
from .patterns.upsidegap2crows import UpsideGap2Crows
from .patterns.counter_attack import CounterAttack
from .patterns.separating_line import SeparatingLine
from .patterns.rising_falling_three_methods import RisingFallingThreeMethods
from .patterns.tasukigap import TasukiGap
from mt5_actions import rates
from mt5_global.settings import timeframe,symbol
import numpy as np
import pandas as pd


class Signal(BearishBullishEnglufing,
        MorningEveningStar, 
        PiercingDarkCloud,
        MorningEveningDoji,
        HammerHangingMan,
        ShootingStartInvertedHammer,
        Harami,
        BeltHold,
        Doji,
        ThreeBlackCrowsThreeAdvancingSolders,
        Unique3River,
        UpsideGap2Crows,
        CounterAttack,
        SeparatingLine,
        RisingFallingThreeMethods,
        TasukiGap):
    def __init__(self):
        self.signal =[]

    def get_signal(self):
        self.signal.append(self.check_bullish_bearish_engulfing(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_morning_evening_star(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_piercing_dark_cloud(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_moring_evining_doji(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_hammer_hanging_man(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_shooting_start_inverted_hammer(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_harami(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_belt_hold(rates.get_curr_rates(symbol,timeframe,14)))
        #self.signal.append(self.check_doji(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_three_black_crows_three_advancing_solders(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_unique_three_river(rates.get_curr_rates(symbol,timeframe,2600)))
        self.signal.append(self.check_upside_gap_2_crows(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_counter_attack(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_separating_line(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_rising_falling_three_methods(rates.get_curr_rates(symbol,timeframe,14)))
        self.signal.append(self.check_tasuki_gap(rates.get_curr_rates(symbol,timeframe,14)))


   
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
            else:
                pass
        if buy > sell:
            signal_type = 'buy'
        elif sell > buy:
            signal_type = 'sell'
        else:
            signal_type = 'hold'
        return signal_type

if __name__ == "__main__":
    signal = Signal()
    print(signal.get_signal())
    print(signal.check_signal_type())