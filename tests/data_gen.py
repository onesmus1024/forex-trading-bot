import pandas as pd
import MetaTrader5 as mt5
import talib as ta

def data_gen():
    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    df = pd.DataFrame(mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M15, 1, 10000))
    df['piercing'] = ta.CDLPIERCING(df['open'], df['high'], df['low'], df['close'])
    df['dark_cloud'] = ta.CDLDARKCLOUDCOVER(df['open'], df['high'], df['low'], df['close'])
    df['morning_star'] = ta.CDLMORNINGSTAR(df['open'], df['high'], df['low'], df['close'])
    df['evening_star'] = ta.CDLEVENINGSTAR(df['open'], df['high'], df['low'], df['close'])
    df['hammer'] = ta.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
    df['hanging_man'] = ta.CDLHANGINGMAN(df['open'], df['high'], df['low'], df['close'])
    df['shooting_star'] = ta.CDLSHOOTINGSTAR(df['open'], df['high'], df['low'], df['close'])
    df['inverted_hammer'] = ta.CDLINVERTEDHAMMER(df['open'], df['high'], df['low'], df['close'])
    df['bullish_engulfing'] = ta.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
    df['morning_doji_star'] = ta.CDLMORNINGDOJISTAR(df['open'], df['high'], df['low'], df['close'])
    df['evening_doji_star'] = ta.CDLEVENINGDOJISTAR(df['open'], df['high'], df['low'], df['close'])
  
    df['belt_hold'] = ta.CDLBELTHOLD(df['open'], df['high'], df['low'], df['close'])
    df['counter_attack'] = ta.CDLCOUNTERATTACK(df['open'], df['high'], df['low'], df['close'])
    df['doji'] = ta.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
    df['harami'] = ta.CDLHARAMI(df['open'], df['high'], df['low'], df['close'])
    df['harami_cross'] = ta.CDLHARAMICROSS(df['open'], df['high'], df['low'], df['close'])
    df['three_black_crows'] = ta.CDL3BLACKCROWS(df['open'], df['high'], df['low'], df['close'])
    df['three_white_soldiers'] = ta.CDL3WHITESOLDIERS(df['open'], df['high'], df['low'], df['close'])
    df['advancing_block'] = ta.CDLADVANCEBLOCK(df['open'], df['high'], df['low'], df['close'])
    df['stalled_pattern'] = ta.CDLSTALLEDPATTERN(df['open'], df['high'], df['low'], df['close'])
    df['unique_three_river'] = ta.CDLUNIQUE3RIVER(df['open'], df['high'], df['low'], df['close'])
    df['upside_gap_two_crows'] = ta.CDLUPSIDEGAP2CROWS(df['open'], df['high'], df['low'], df['close'])
    df.to_csv('C:/mt5_bots/mt5_EA_v3/data/data.csv')




if __name__ == '__main__':
    data_gen()    