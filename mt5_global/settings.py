import MetaTrader5 as mt5
import datetime
import pytz
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M15

Model_type = "v3_LSTM"
time_series = 15
Debug = False

timezone = pytz.timezone("Etc/UTC")
utc_from = datetime.datetime(2020, 3, 1, tzinfo=timezone)