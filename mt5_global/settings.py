import MetaTrader5 as mt5
import datetime
import pytz
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M10

Model_type = "v3_LSTM"
time_series = 5
Debug = False

timezone = pytz.utc
utc_from = datetime.datetime(2022, 1,1, tzinfo=timezone)