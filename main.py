import numpy as np
import pandas as pd
from tensorflow import keras
import datetime
import time
import pytz
import MetaTrader5 as mt5
from models.model import model
from mt5_actions.authorize import login
from mt5_actions.tick import get_curr_ticks
from mt5_actions.rates import get_curr_rates
from mt5_actions.order import buy_order, sell_order, check_order
from mt5_global.settings import symbol, timeframe
from models.model import scaler


saved_model = None

saved_model = keras.models.load_model("C:\mt5_Bots\mt5_EA_v4\models\saved_models\EURUSD-run_2022_11_05-13_51_58")

# order parameters
lot = 0.1
point = mt5.symbol_info(symbol).point



def trade():
    if not login():
        print('login failed')
        return
    rates = get_curr_rates(symbol,timeframe, 1)
    while True:
        try:
            curr_rate =get_curr_rates(symbol,timeframe, 1)
            curr_rate_frame = pd.DataFrame(curr_rate)
            previous_rates_frame = pd.DataFrame(rates)
            if int(curr_rate_frame['time'])== int(previous_rates_frame['time']):
                time.sleep(2)
                continue

            #drop time column
            previous_rates_frame=previous_rates_frame.drop(['time','close'], axis=1)
        
            #scale data
            x_scaled = scaler.transform(previous_rates_frame)
            x = pd.DataFrame(x_scaled, columns=['open','high','low','tick_volume','spread','real_volume'])
            #predict
            prediction = model.predict(x)
            prediction = round(prediction[0][0],5)
            #get current price
            curr_price = mt5.symbol_info_tick(symbol).ask
            order_dic = check_order()
            if prediction > curr_price:
                if order_dic['buy']:
                    print('buy order already exists')
                    continue
                buy_order(prediction,symbol)
            elif prediction < curr_price:
                if order_dic['sell']:
                    print('sell order already exists')
                    
                    continue
                sell_order(prediction,symbol)
            else:
                print('no action')
            rates = get_curr_rates(symbol,timeframe, 1)
        except Exception as e:
            print(e)
            print("order failed")
            time.sleep(2)
            pass
        



if __name__ == "__main__":
    trade()
   
       

