import talib as ta
class BearishBullishEnglufing:
    def check_bearish_bullish(self,df) -> dict:
        """
        Bearish and Bullish Engulfing Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        # Check if the candle is a bearish engulfing pattern
        # If the candle is a bearish engulfing pattern, return dict {'buy': 0, 'sell': 1}
        # Else return dict {'buy': 0, 'sell': 0}
        # Check if the candle is a bearish engulfing pattern
        if ta.CDLENGULFING(df['open'], df['high'], df['low'], df['close']) == -100:
            return {'buy': 0, 'sell': 1,'pattern':'bearish engulfing'}
        # Check if the candle is a bullish engulfing pattern
        elif ta.CDLENGULFING(df['open'], df['high'], df['low'], df['close']) == 100:
            return {'buy': 1, 'sell': 0,'pattern':'bullish engulfing'}
        else:
            return {'buy': 0, 'sell': 0,'pattern':"bearish or bullish engulfing not found"}
    