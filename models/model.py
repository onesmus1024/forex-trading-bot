import MetaTrader5 as mt5
import ta
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


#set freq
#rates_frame.index = pd.DatetimeIndex(rates_frame.index).to_period('H')
#rates_frame.index.freq = 'H'

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
    #replace scaled close with original close
    #print close column
    print("#@@"*50)
    #print close column
    print(scaled_data[:,3][:20])
    print(scaled_data.shape)
    return scaled_data

def time_series_generator(scaled_data):
    global x_train
    global y_train
    #generate time series where y is the next value of x in 3 column of scaled_data
    for i in range(time_series,scaled_data.shape[0],time_series):
        x_train.append(scaled_data[i-time_series:i-1,:])
        y_train.append(scaled_data[:,3][i])

    x_train,y_train = np.array(x_train),np.array(y_train)
    #print y_train
    print("!!@@"*50)
    print(y_train[:10])
    time.sleep(120)
    return x_train,y_train


#build model
def build_model(x_train,y_train):
    global history
    global model
    model = keras.models.Sequential([
   # keras.layers.Conv1D(filters=20, kernel_size=4, strides=2, padding="valid",
    #input_shape=[settings.time_series, 10]),
    keras.layers.GRU(20,return_sequences=True,input_shape=[x_train.shape[1],x_train.shape[2]]),
    keras.layers.LSTM(256,activation='relu'),
    keras.layers.Dense(64,activation='relu'),
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




