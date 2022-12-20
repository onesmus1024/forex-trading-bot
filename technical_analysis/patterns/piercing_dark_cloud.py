import talib as ta
class PiercingDarkCloud:
    def check_piercing_Dark_cloud(self, df):
        # Check if the candle is a piercing pattern
        # If the candle is a piercing pattern, return dict {'buy': 1, 'sell': 0}
        # Else return dict {'buy': 0, 'sell': 0}
        # Check if the candle is a dark cloud pattern or piercing pattern
        if ta.CDLPIERCING(df['open'], df['high'], df['low'], df['close']) == 100:
            return {'buy': 1, 'sell': 0,'pattern':'piercing'}
        elif ta.CDLDARKCLOUDCOVER(df['open'], df['high'], df['low'], df['close']) == -100:
            return {'buy': 0, 'sell': 1,'pattern':'dark cloud'}
        else:
            return {'buy': 0, 'sell': 0,'pattern':"piercing or dark cloud not found"}