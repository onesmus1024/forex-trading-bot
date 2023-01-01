import MetaTrader5 as mt5
import datetime
import pytz
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M15
sl=0.0
Model_type = "v3_LSTM"
time_series = 1
period = 14
n_future = 1
Debug = True
Trade_with_signals = True
timezone = pytz.utc
utc_from = datetime.datetime(2022, 12,1, tzinfo=timezone)