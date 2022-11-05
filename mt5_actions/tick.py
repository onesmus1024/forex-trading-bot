import MetaTrader5 as mt5


def get_curr_ticks(symbol,utc_from, count):
    ticks = mt5.copy_ticks_from(symbol, mt5.TIMEFRAME_H1, utc_from, count)
    return ticks    