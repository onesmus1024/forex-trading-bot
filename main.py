import numpy as np
import pandas as pd
import logging
import time
import datetime
import MetaTrader5 as mt5
from models.model import model
from mt5_actions.authorize import login
from mt5_actions.rates import get_curr_rates
from mt5_actions.order import buy_order, sell_order, check_order
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

    rates = get_curr_rates(symbol,timeframe, time_series)
    while True:
        try:
            signal = Signal()
            signal.get_signal()
            curr_rate =get_curr_rates(symbol,timeframe, time_series)
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
        
            previous_rates_frame=previous_rates_frame.drop(['real_volume'], axis=1)
            previous_rates_frame['momentum'] = previous_rates_frame['open'] - previous_rates_frame['close']
            previous_rates_frame['average'] = (previous_rates_frame['high'] + previous_rates_frame['low'])/2
            previous_rates_frame['range'] = previous_rates_frame['high'] - previous_rates_frame['low']
            previous_rates_frame['ohlc'] = (previous_rates_frame['open'] + previous_rates_frame['high'] + previous_rates_frame['low'] + previous_rates_frame['close'])/4
        
            previous_rates_frame['time'] = pd.to_datetime(previous_rates_frame['time'], unit='s')
            previous_rates_frame = previous_rates_frame.set_index('time')
            x = scaler.transform(previous_rates_frame)
            x = x.reshape(x.shape[0],x.shape[1],time_series)
            #predict
            prediction = model.predict(x) #scale back
            print("prediction: ",prediction)
            prediction_copies = np.repeat(prediction,10, axis=-1)
            prediction = scaler.inverse_transform(prediction_copies)

            print("prediction: ",prediction)
            
            prediction = np.round(prediction[-1][3],5)
            #get current price
            curr_price = mt5.symbol_info_tick(symbol).ask
            curr_price_bid = mt5.symbol_info_tick(symbol).bid
            print("#"*50)
            print('prediction: ',prediction)
            print('current ask price: ',curr_price)
            print('current bid price: ',curr_price_bid)
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
            if prediction > mt5.symbol_info_tick(symbol).ask:
                if order_dic['buy']:
                    print('buy order already exists')
                    continue
                buy_order(prediction,symbol)
            elif prediction < mt5.symbol_info_tick(symbol).bid:
                if order_dic['sell']:
                    print('sell order already exists')
                    
                    continue
                sell_order(prediction,symbol)
            else:
                print('no action')
            rates = get_curr_rates(symbol,timeframe, time_series)
        except Exception as e:
            #log the error to error.log file using python logging module
            logging.basicConfig(filename='C:\mt5_bots\mt5_EA_v3\logs_dir\error.log',level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',)
            logging.exception(e)

            print("order failed")
            time.sleep(2)
            pass

def trade_with_signal():
    rates = get_curr_rates(symbol,timeframe, time_series)
    print('.... waiting for signal ....')
    while True:
        try:
            #check for spread if spread is greater than 5 pips do not trade
            
            curr_rate =get_curr_rates(symbol,timeframe, time_series)
            curr_rate_frame = pd.DataFrame(curr_rate)
            curr_rate_frame_last = curr_rate_frame.tail(1)
            previous_rates_frame = pd.DataFrame(rates)
            previous_rates_frame_last = previous_rates_frame.tail(1)
            if int(curr_rate_frame_last['time'])== int(previous_rates_frame_last['time']):
                time.sleep(2)
                continue
            if mt5.symbol_info_tick(symbol).ask - mt5.symbol_info_tick(symbol).bid < 20:
                signal = Signal()
                signal.get_signal()
                
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
                rates = get_curr_rates(symbol,timeframe, time_series)
                print('.... waiting for another signal ....')
            else:
                print('spread is greater than 5 pips')
                continue
        except Exception as e:
            #log the error to error.log file using python logging module
            logging.basicConfig(filename='C:\mt5_bots\mt5_EA_v3\logs_dir\error.log',level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',)
            logging.exception(e)

            print("order failed")
            rates = get_curr_rates(symbol,timeframe, time_series)
            continue



if __name__ == "__main__":
    if Trade_with_signals:
        trade_with_signal()
    else:
        trade()
   
       

