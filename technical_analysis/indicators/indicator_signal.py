import logging
import sys

from mt5_actions import rates
from mt5_global.settings import timeframe,symbol
import pathlib
from technical_analysis.indicators.moving_average import MovingAverage
from technical_analysis.indicators.relative_strength_index import RelativeStrengthIndex
from technical_analysis.indicators.e_moving_average14_e_moving_average28 import EMA14_EMA28


class IndicatorSignal(
    MovingAverage,
    RelativeStrengthIndex,
    EMA14_EMA28
):
    def __init__(self):
        super().__init__()
        self.indicator_signal = []
    def get_indicator_signal(self):
        self.indicator_signal.append(self.check_ma(rates.get_curr_rates(symbol,timeframe,14)))
        self.indicator_signal.append(self.check_rsi(rates.get_curr_rates(symbol,timeframe,14)))
        self.indicator_signal.append(self.check_ema())
        #log the indicator signal in indicator.log file
        logging.basicConfig(
            filename='C:\mt5_bots\mt5_EA_v3\logs_dir\indicator.log', level=logging.INFO)
        logging.info(self.indicator_signal)

    
    def check_indicator_signal(self):
        buy = 0
        sell = 0
        for i in self.indicator_signal:
            if i['buy'] == 1:
                buy += 1
                sell-=1
            elif i['sell'] == 1:
                sell += 1
                buy -= 1
            else:
                pass
        if buy > sell:
            return 'buy'
        elif sell > buy:
            return 'sell'
        else:
            return 'hold'