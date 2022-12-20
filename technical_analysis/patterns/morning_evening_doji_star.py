import talib as ta
class MorningEveningDoji:
    def check_morning_evening_doji(self,df)->dict:
        """
        Morning and Evening Doji Star Pattern
        :param df: pandas.DataFrame
        :return: dict
        """
        # Check if the candle is a morning doji star pattern
        # If the candle is a morning doji star pattern, return dict {'buy': 1, 'sell': 0}
        # Else return dict {'buy': 0, 'sell': 0}
        # Check if the candle is a morning doji star pattern
        if ta.CDLMORNINGDOJISTAR(df['open'], df['high'], df['low'], df['close']) == 100:
            return {'buy': 1, 'sell': 0,'pattern':'morning doji star'}
        # Check if the candle is a evening doji star pattern
        elif ta.CDLEVENINGDOJISTAR(df['open'], df['high'], df['low'], df['close']) == -100:
            return {'buy': 0, 'sell': 1,'pattern':'evening doji star'}
        else:
            return {'buy': 0, 'sell': 0,'pattern':"morning or evening doji star not found"}
