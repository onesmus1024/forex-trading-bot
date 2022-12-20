import MetaTrader5 as mt5
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from pandas.plotting import scatter_matrix
import numpy as np
import matplotlib.pyplot as plt
import datetime

from mt5_global import settings
import time
import os
import talib as ta


from mt5_actions.rates import get_rates
from mt5_global.settings import symbol, timeframe,utc_from,timezone,Debug,time_series


#tset time zone to UTC
utc_to = datetime.datetime.now(tz=timezone)
root_dir = os.path.join(os.curdir,"models/saved_models")
model= None
history = None
scaler = None
x_train = []
y_train = []

#get rates from mt5
rates = get_rates(symbol,timeframe, utc_from, utc_to)

# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates) 
print(rates_frame.head())
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
rates_frame.drop(['real_volume'],axis=1,inplace=True)
rates_frame = rates_frame.set_index('time')
rates_frame['momentum'] = rates_frame['open'] - rates_frame['close']
rates_frame['average'] = (rates_frame['high'] + rates_frame['low'])/2
rates_frame['range'] = rates_frame['high'] - rates_frame['low']
rates_frame['ohlc'] = (rates_frame['open'] + rates_frame['high'] + rates_frame['low'] + rates_frame['close'])/4
#add buy and sell signals
rates_frame['buy'] = np.where(rates_frame['close'] > rates_frame['open'],1,0)
rates_frame['sell'] = np.where(rates_frame['close'] < rates_frame['open'],1,0)
#add patterns from talib
rates_frame['morning_star'] = ta.CDLMORNINGSTAR(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
rates_frame['evening_star'] = ta.CDLEVENINGSTAR(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
rates_frame['morning_doji_star'] = ta.CDLMORNINGDOJISTAR(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
rates_frame['evening_doji_star'] = ta.CDLEVENINGDOJISTAR(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Two Crows
rates_frame['two_crows'] = ta.CDL2CROWS(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Three Black Crows
rates_frame['three_black_crows'] = ta.CDL3BLACKCROWS(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Three Inside Up/Down
rates_frame['three_inside_up_down'] = ta.CDL3INSIDE(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Three-Line Strike
rates_frame['three_line_strike'] = ta.CDL3LINESTRIKE(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Three Outside Up/Down
rates_frame['three_outside_up_down'] = ta.CDL3OUTSIDE(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Three Stars In The South
rates_frame['three_stars_in_the_south'] = ta.CDL3STARSINSOUTH(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Three Advancing White Soldiers
rates_frame['three_advancing_white_soldiers'] = ta.CDL3WHITESOLDIERS(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Abandoned Baby
rates_frame['abandoned_baby'] = ta.CDLABANDONEDBABY(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Advance Block
rates_frame['advance_block'] = ta.CDLADVANCEBLOCK(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Belt-hold
rates_frame['belt_hold'] = ta.CDLBELTHOLD(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Breakaway
rates_frame['breakaway'] = ta.CDLBREAKAWAY(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Closing Marubozu
rates_frame['closing_marubozu'] = ta.CDLCLOSINGMARUBOZU(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Concealing Baby Swallow
rates_frame['concealing_baby_swallow'] = ta.CDLCONCEALBABYSWALL(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Counterattack
rates_frame['counterattack'] = ta.CDLCOUNTERATTACK(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Dark Cloud Cover
rates_frame['dark_cloud_cover'] = ta.CDLDARKCLOUDCOVER(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Doji
rates_frame['doji'] = ta.CDLDOJI(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Doji Star
rates_frame['doji_star'] = ta.CDLDOJISTAR(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Dragonfly Doji
rates_frame['dragonfly_doji'] = ta.CDLDRAGONFLYDOJI(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Engulfing Pattern
rates_frame['engulfing_pattern'] = ta.CDLENGULFING(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Evening Doji Star
rates_frame['evening_doji_star'] = ta.CDLEVENINGDOJISTAR(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Evening Star
rates_frame['evening_star'] = ta.CDLEVENINGSTAR(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Up/Down-gap side-by-side white lines
rates_frame['up_down_gap_side_by_side_white_lines'] = ta.CDLGAPSIDESIDEWHITE(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Gravestone Doji
rates_frame['gravestone_doji'] = ta.CDLGRAVESTONEDOJI(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])
#Hammer
rates_frame['hammer'] = ta.CDLHAMMER(rates_frame['open'], rates_frame['high'], rates_frame['low'], rates_frame['close'])

def data_stats(rates_frame):
    print(rates_frame.describe())
    print(rates_frame.info())
    print(rates_frame.corr())
    corretion_matrix =rates_frame.corr()
    print(corretion_matrix['close'].sort_values(ascending=False))
   
def model_stats(model):
    print(model.summary())
    print(model.get_config())
    print(model.get_weights())

def data_visualization(rates_frame):
   # results = seasonal_decompose(rates_frame['close'])
    #results.plot()
    plt.show()
    rates_frame['close'].plot()
    rates_frame['open'].plot()
    rates_frame['high'].plot()
    rates_frame['low'].plot()
    plt.legend()
    plt.show()
    

def data_preparation(rates_frame):
    global scaler
    scaler = MinMaxScaler()
    scaled_data = scaler.fit(rates_frame)
    scaled_data = scaler.transform(rates_frame)
   
    return scaled_data

def time_series_generator(scaled_data):
    global x_train
    global y_train
    #generate time series where y is the next value of x in 3 column of scaled_data
    for i in range(time_series,scaled_data.shape[0],time_series):
        x_train.append(scaled_data[i-time_series:i-1,:])
        y_train.append(scaled_data[:,3][i])

    x_train,y_train = np.array(x_train),np.array(y_train)
 
    return x_train,y_train


#build model
def build_model(x_train,y_train):
    global history
    global model
    model = keras.models.Sequential([
   # keras.layers.Conv1D(filters=20, kernel_size=4, strides=2, padding="valid",
    #input_shape=[settings.time_series, 10]),
    keras.layers.GRU(20,return_sequences=True,input_shape=[x_train.shape[1],x_train.shape[2]]),
    keras.layers.LSTM(256),
    keras.layers.Dense(64),
    keras.layers.Dense(1)
    ])
    model.summary()
    model.compile(optimizer='adam',loss='mse',metrics=['mae'])
    history = model.fit(x_train,y_train,epochs=10,validation_split=0.1)


def get_run_logdir():
    run_id =symbol+"-"+time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return run_id
#save model
def save_model(model):
    model.save(os.path.join(root_dir,get_run_logdir()))

def plot_learning_curves(history):
    plt.plot(history.history['loss'],label='loss',color='red')
    plt.plot(history.history['val_loss'],label='val_loss',color='blue')
    plt.legend()
    #plt.gca().set_ylim(0,0.001)
    plt.show()
    #score = model.evaluate(x_test,y_test)
    #print(score)

def main():
    data_stats(rates_frame)
    #data_visualization(rates_frame)
    scaled_data = data_preparation(rates_frame)
   
    x_train,y_train = time_series_generator(scaled_data)
    build_model(x_train,y_train)
    #model_stats(model)
    if settings.Debug:
        plot_learning_curves(history)
        

    if settings.Debug == False:
        save_model(model)


main()




