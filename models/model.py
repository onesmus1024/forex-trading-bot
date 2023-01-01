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
from mt5_global.settings import symbol, timeframe,utc_from,timezone,Debug,time_series,Trade_with_signals


#tset time zone to UTC
utc_to = datetime.datetime.now(tz=timezone)
root_dir = os.path.join(os.curdir,"models/saved_models")
model= None
history = None
scaler = None
x_train = None
y_train = None

#get rates from mt5
rates = get_rates(symbol,timeframe, utc_from, utc_to)

# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates) 
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
rates_frame.drop(['real_volume'],axis=1,inplace=True)
rates_frame = rates_frame.set_index('time')
rates_frame['momentum'] = rates_frame['open'] - rates_frame['close']
rates_frame['average'] = (rates_frame['high'] + rates_frame['low'])/2
rates_frame['range'] = rates_frame['high'] - rates_frame['low']
rates_frame['ohlc'] = (rates_frame['open'] + rates_frame['high'] + rates_frame['low'] + rates_frame['close'])/4



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
    #print first 10 rows of scaled data

    return scaled_data

def time_series_generator(scaled_data):
    global x_train
    global y_train
    x_train = scaled_data
    y_train = scaled_data[:,3]
    x_train= x_train.reshape(x_train.shape[0],x_train.shape[1],settings.time_series)
    #pop the last row of x_train
    x_train = np.delete(x_train,-1,0)
    #pop the first value of y_train
    y_train = np.delete(y_train,0)

    #confirm that y_train are the next value of x_train close
    #for i in range(len(scaled_data)):
        #if x_train[i+1][3][0] == y_train[i]:
            #print("true")
            #time.sleep(10)
        #else:
            #print("false")
            #time.sleep(10)

   
    return x_train,y_train
#callback for early stopping
def early_stopping():
    early_stopping_cb = keras.callbacks.EarlyStopping(patience=10,restore_best_weights=True)
    return early_stopping_cb

#build model
def build_model(x_train,y_train):
    global history
    global model
    model = keras.models.Sequential([
   # keras.layers.Conv1D(filters=20, kernel_size=4, strides=2, padding="valid",
    #input_shape=[settings.time_series, 10]),
    keras.layers.GRU(20,return_sequences=True,input_shape=[x_train.shape[1],settings.time_series]),
    keras.layers.LSTM(25),
    keras.layers.Dense(64),
    keras.layers.Dense(1)
    ])
    model.summary()
    model.compile(optimizer='adam',loss='mse',metrics=['mae'])
    history = model.fit(x_train,y_train,epochs=100,validation_split=0.1,batch_size=32,shuffle=False)


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


if not Trade_with_signals:
    main()




