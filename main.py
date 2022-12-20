import numpy as np
import pandas as pd
import time
import datetime
import MetaTrader5 as mt5
from models.model import model
from mt5_actions.authorize import login
from mt5_actions.tick import get_curr_ticks
from mt5_actions.rates import get_curr_rates
from mt5_actions.order import buy_order, sell_order, check_order, close_position
from mt5_global.settings import symbol, timeframe,time_series,Debug,timezone,Trade_with_signals
from models.model import scaler
import schedule
import talib as ta
from technical_analysis.signal import Signal

saved_model = None
def trade_time():
    print("executing")

    while True:
        if datetime.datetime.now().weekday in [1,2,3,4,5] and datetime.datetime.now().hour in range(8,17):
            trade()
        else:
            #sleep for 1 hour
            print('sleeping for one hour')
            time.sleep(3600)
            continue
        

def trade():
    if not login():
        print('login failed')
        return

    rates = get_curr_rates(symbol,timeframe, time_series-1)
    while True:
        try:
            signal = Signal()
            signal.get_signal()
            curr_rate =get_curr_rates(symbol,timeframe, time_series-1)
            curr_rate_frame = pd.DataFrame(curr_rate)
            curr_rate_frame_last = curr_rate_frame.tail(1)
            previous_rates_frame = pd.DataFrame(rates)
            previous_rates_frame_last = previous_rates_frame.tail(1)
            if int(curr_rate_frame_last['time'])== int(previous_rates_frame_last['time']):
                time.sleep(2)
                continue
            
            with open('C:\mt5_bots\mt5_EA_v3\logs_dir\signal.log','a') as f:
                f.write(str(datetime.datetime.now(timezone)))
                f.write(str(Signal().get_signal()))
                #add new line
                f.write('\n')
            #drop time column
            previous_rates_frame=previous_rates_frame.drop(['real_volume'], axis=1)
            previous_rates_frame['momentum'] = previous_rates_frame['open'] - previous_rates_frame['close']
            previous_rates_frame['average'] = (previous_rates_frame['high'] + previous_rates_frame['low'])/2
            previous_rates_frame['range'] = previous_rates_frame['high'] - previous_rates_frame['low']
            previous_rates_frame['ohlc'] = (previous_rates_frame['open'] + previous_rates_frame['high'] + previous_rates_frame['low'] + previous_rates_frame['close'])/4
                    #add buy and sell signals
            previous_rates_frame['buy'] = np.where(previous_rates_frame['close'] > previous_rates_frame['open'],1,0)
            previous_rates_frame['sell'] = np.where(previous_rates_frame['close'] < previous_rates_frame['open'],1,0)
            #add patterns from talib
            previous_rates_frame['morning_star'] = ta.CDLMORNINGSTAR(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            previous_rates_frame['evening_star'] = ta.CDLEVENINGSTAR(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            previous_rates_frame['morning_doji_star'] = ta.CDLMORNINGDOJISTAR(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            previous_rates_frame['evening_doji_star'] = ta.CDLEVENINGDOJISTAR(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Two Crows
            previous_rates_frame['two_crows'] = ta.CDL2CROWS(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Three Black Crows
            previous_rates_frame['three_black_crows'] = ta.CDL3BLACKCROWS(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Three Inside Up/Down
            previous_rates_frame['three_inside_up_down'] = ta.CDL3INSIDE(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Three-Line Strike
            previous_rates_frame['three_line_strike'] = ta.CDL3LINESTRIKE(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Three Outside Up/Down
            previous_rates_frame['three_outside_up_down'] = ta.CDL3OUTSIDE(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Three Stars In The South
            previous_rates_frame['three_stars_in_the_south'] = ta.CDL3STARSINSOUTH(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Three Advancing White Soldiers
            previous_rates_frame['three_advancing_white_soldiers'] = ta.CDL3WHITESOLDIERS(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Abandoned Baby
            previous_rates_frame['abandoned_baby'] = ta.CDLABANDONEDBABY(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Advance Block
            previous_rates_frame['advance_block'] = ta.CDLADVANCEBLOCK(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Belt-hold
            previous_rates_frame['belt_hold'] = ta.CDLBELTHOLD(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Breakaway
            previous_rates_frame['breakaway'] = ta.CDLBREAKAWAY(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Closing Marubozu
            previous_rates_frame['closing_marubozu'] = ta.CDLCLOSINGMARUBOZU(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Concealing Baby Swallow
            previous_rates_frame['concealing_baby_swallow'] = ta.CDLCONCEALBABYSWALL(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Counterattack
            previous_rates_frame['counterattack'] = ta.CDLCOUNTERATTACK(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Dark Cloud Cover
            previous_rates_frame['dark_cloud_cover'] = ta.CDLDARKCLOUDCOVER(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Doji
            previous_rates_frame['doji'] = ta.CDLDOJI(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Doji Star
            previous_rates_frame['doji_star'] = ta.CDLDOJISTAR(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Dragonfly Doji
            previous_rates_frame['dragonfly_doji'] = ta.CDLDRAGONFLYDOJI(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Engulfing Pattern
            previous_rates_frame['engulfing_pattern'] = ta.CDLENGULFING(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Evening Doji Star
            previous_rates_frame['evening_doji_star'] = ta.CDLEVENINGDOJISTAR(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Evening Star
            previous_rates_frame['evening_star'] = ta.CDLEVENINGSTAR(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Up/Down-gap side-by-side white lines
            previous_rates_frame['up_down_gap_side_by_side_white_lines'] = ta.CDLGAPSIDESIDEWHITE(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Gravestone Doji
            previous_rates_frame['gravestone_doji'] = ta.CDLGRAVESTONEDOJI(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])
            #Hammer
            previous_rates_frame['hammer'] = ta.CDLHAMMER(previous_rates_frame['open'], previous_rates_frame['high'], previous_rates_frame['low'], previous_rates_frame['close'])

            #drop time column
            previous_rates_frame['time'] = pd.to_datetime(previous_rates_frame['time'], unit='s')
            previous_rates_frame = previous_rates_frame.set_index('time')
            x = scaler.transform(previous_rates_frame)
            x = x.reshape(1,time_series-1,38)
            #predict
            prediction = model.predict(x) #scale back
            print("prediction: ",prediction)
            prediction_copies = np.repeat(prediction,38, axis=-1)
            prediction = scaler.inverse_transform(prediction_copies)

            print("prediction: ",prediction)
            
            prediction = np.round(prediction[-1][3],5)
            #get current price
            curr_price = curr_rate_frame_last['open'].values[0]
            print("#"*50)
            print('prediction: ',prediction)
            print('current price: ',curr_price)
            #log prediction,current price and signal type to signal_prediction.log
            with open('C:\mt5_bots\mt5_EA_v3\logs_dir\signal_prediction.log','a') as f:
                f.write(str(datetime.datetime.now(timezone)))
                if prediction > curr_price:
                    f.write('buy')
                elif prediction < curr_price:
                    f.write('sell')
                f.write(str(signal.check_signal_type()))
                #add new line
                f.write('\n')

            order_dic = check_order()
            if prediction > mt5.symbol_info_tick(symbol).ask and prediction> mt5.symbol_info_tick(symbol).bid :
                buy_order(prediction,symbol)
               
            elif prediction < mt5.symbol_info_tick(symbol).ask and prediction< mt5.symbol_info_tick(symbol).bid :
               
                sell_order(prediction,symbol)
            elif signal.check_signal_type() == 'hold':
                print('hold no signal')
            else:
                print('No action as price changed before order was placed')
            rates = get_curr_rates(symbol,timeframe, time_series-1)
        except Exception as e:
            print(e)
            print("order failed")
            time.sleep(2)
            pass

def trade_with_signal():
    rates = get_curr_rates(symbol,timeframe, time_series-1)
    while True:
        try:
            signal = Signal()
            signal.get_signal()
            
            
            curr_rate =get_curr_rates(symbol,timeframe, time_series-1)
            curr_rate_frame = pd.DataFrame(curr_rate)
            curr_rate_frame_last = curr_rate_frame.tail(1)
            previous_rates_frame = pd.DataFrame(rates)
            previous_rates_frame_last = previous_rates_frame.tail(1)
            if int(curr_rate_frame_last['time'])== int(previous_rates_frame_last['time']):
                time.sleep(2)
                continue
            #log signal to signal.log
            with open('C:\mt5_bots\mt5_EA_v3\logs_dir\signal.log','a') as f:
                f.write(str(datetime.datetime.now(timezone)))
                f.write(str(Signal().get_signal()))
                #add new line
                f.write('\n')
            if signal.check_signal_type() == 'buy':
                price = mt5.symbol_info_tick(symbol).ask+0.00100
                buy_order(price,symbol)
            elif signal.check_signal_type() == 'sell':
                price = mt5.symbol_info_tick(symbol).bid-0.00100
                sell_order(price,symbol)
            else:
                print('no signal')
            rates = get_curr_rates(symbol,timeframe, time_series-1)
        except Exception as e:
            print(e)
            print("order failed")
            time.sleep(2)
            pass



if __name__ == "__main__":
    if Trade_with_signals:
        trade_with_signal()
    else:
        trade()
   
       

