import talib as ta
import MetaTrader5 as mt5
class MorningEveningStar:
    def check_morning_evening_star(self, df) -> dict:
        """
        Morning and Evening Star Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        # Check if the candle is a morning star pattern from the last 3 candles using talib
        # If the candle is a morning star pattern, return dict {'buy': 1, 'sell': 0}
        # Else return dict {'buy': 0, 'sell': 0}
        # Check if the candle is a morning star pattern
        if ta.CDLMORNINGSTAR(df['open'], df['high'], df['low'], df['close']) == 100:
            return {'buy': 1, 'sell': 0,'pattern':'morning star'}
        # Check if the candle is a evening star pattern
        elif ta.CDLEVENINGSTAR(df['open'], df['high'], df['low'], df['close']) == -100:
            return {'buy': 0, 'sell': 1,'pattern':'evening star'}
        else:
            return {'buy': 0, 'sell': 0,'pattern':"morning or evening star not found"}
     

if __name__ == "__main__":
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    morning_evening_star = MorningEveningStar()
    print(morning_evening_star.check_morning_evening_star(mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M10, 0, 1)))
    print(mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M10, 0, 1))