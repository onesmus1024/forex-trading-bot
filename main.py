import numpy as np
import pandas as pd
import time
import MetaTrader5 as mt5
from models.model import model
from mt5_actions.authorize import login
from mt5_actions.tick import get_curr_ticks
from mt5_actions.rates import get_curr_rates
from mt5_actions.order import buy_order, sell_order, check_order
from mt5_global.settings import symbol, timeframe,time_series,Debug
from models.model import scaler


saved_model = None

def trade():
    if not login():
        print('login failed')
        return
    rates = get_curr_rates(symbol,timeframe, time_series)
    while True:
        try:
            
            curr_rate =get_curr_rates(symbol,timeframe, time_series)
            curr_rate_frame = pd.DataFrame(curr_rate)
            curr_rate_frame_last = curr_rate_frame.tail(1)
            previous_rates_frame = pd.DataFrame(rates)
            previous_rates_frame_last = previous_rates_frame.tail(1)
            if int(curr_rate_frame_last['time'])== int(previous_rates_frame_last['time']):
                time.sleep(2)
                continue

            #drop time column
            previous_rates_frame=previous_rates_frame.drop(['real_volume'], axis=1)
            previous_rates_frame['momentum'] = previous_rates_frame['open'] - previous_rates_frame['close']
            previous_rates_frame['average'] = (previous_rates_frame['high'] + previous_rates_frame['low'])/2
            previous_rates_frame['range'] = previous_rates_frame['high'] - previous_rates_frame['low']
            previous_rates_frame['ohlc'] = (previous_rates_frame['open'] + previous_rates_frame['high'] + previous_rates_frame['low'] + previous_rates_frame['close'])/4

            #drop time column
            previous_rates_frame['time'] = pd.to_datetime(previous_rates_frame['time'], unit='s')
            previous_rates_frame = previous_rates_frame.set_index('time')
            x = scaler.transform(previous_rates_frame)
            x = np.reshape(x, (1, time_series, 10))
       
            #predict
            prediction = model.predict(x) #scale back

            prediction_copies = np.repeat(prediction, 10, axis=-1)
            prediction = scaler.inverse_transform(prediction_copies)

            print("prediction: ",prediction)
            
            prediction = np.round(prediction[-1][0],5)
            #get current price
            curr_price = curr_rate_frame_last['open'].values[0]
            print("#"*50)
            print('prediction: ',prediction)
            print('current price: ',curr_price)
            

            order_dic = check_order()
            if prediction > mt5.symbol_info_tick(symbol).ask and prediction> mt5.symbol_info_tick(symbol).bid:
                if order_dic['buy']:
                    print('buy order already exists')
                    rates = get_curr_rates(symbol,timeframe, time_series)
                    continue
                buy_order(prediction,symbol)
            elif prediction < curr_price:
                if order_dic['sell']:
                    print('sell order already exists')
                    rates = get_curr_rates(symbol,timeframe, time_series)
                    continue
                sell_order(prediction,symbol)
            else:
                print('no action')
            rates = get_curr_rates(symbol,timeframe, time_series)
        except Exception as e:
            print(e)
            print("order failed")
            time.sleep(2)
            pass
        



if __name__ == "__main__":
    trade()
   
       

