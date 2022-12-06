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
import pytz
from mt5_global import settings
import time
import os
from keras.preprocessing.sequence import TimeseriesGenerator
from statsmodels.tsa.seasonal import seasonal_decompose


from mt5_actions.rates import get_rates
from mt5_global.settings import symbol, timeframe,utc_from,timezone,Debug


#tset time zone to UTC
utc_to = datetime.datetime.now(tz=timezone)
root_dir = os.path.join(os.curdir,"models/saved_models")
model= None
history = None
scaler = None


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
y_data = rates_frame['close']

#set freq
#rates_frame.index = pd.DatetimeIndex(rates_frame.index).to_period('H')
#rates_frame.index.freq = 'H'

def data_stats(rates_frame):
    print(rates_frame.describe())
    print(rates_frame.info())
    print(rates_frame.corr())
    corretion_matrix =rates_frame.corr()
    #time     open     high      low    close  tick_volume  spread  real_volume
    #scatter_matrix(rates_frame[attributes],figsize=(12,8))
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
    #plot data
    rates_frame.plot(subplots=True)
    plt.show()
    #plot histogram
    rates_frame.hist()
    plt.show()
    #plot scatter matrix
    scatter_matrix(rates_frame)
    plt.show()

def data_preparation(rates_frame,y_data):
    global scaler
    scaler = MinMaxScaler()
    scaler.fit(rates_frame)
    scaled_data = scaler.transform(rates_frame)
    y_scaled=scaled_data[:,3]
    print(scaled_data)
    data_length = len(scaled_data)
    split_at = int(data_length*0.8)

    #split data
    x_train = scaled_data[:split_at]
    x_test = scaled_data[split_at:]
    train_y = y_scaled[:split_at]
    test_y = y_scaled[split_at:]
    return x_train,x_test,train_y,test_y

def train_time_series_generator(x_train,y_train):
    n_input = settings.time_series
    generator = TimeseriesGenerator(x_train,y_train,length=n_input,batch_size=1)
   
   
 
  
    return generator
def test_time_series_generator(x_test,y_test):
    n_input = settings.time_series
    generator = TimeseriesGenerator(x_test,y_test,length=n_input,batch_size=1)
    

    return generator

#build model
def build_model(x_train,y_train,x_test,y_test):
    global history
    global model
    model = keras.models.Sequential([
   # keras.layers.Conv1D(filters=20, kernel_size=4, strides=2, padding="valid",
    #input_shape=[settings.time_series, 10]),
    keras.layers.GRU(20,return_sequences=True,input_shape=[settings.time_series,10]),
    keras.layers.LSTM(256),
    keras.layers.Dense(64),
    keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam',loss='mse',metrics=['mae'])
    history = model.fit(train_time_series_generator(x_train,y_train),epochs=1,validation_data=test_time_series_generator(x_test,y_test))


def get_run_logdir():
    run_id =symbol+"-"+time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return run_id
#save model
def save_model(model):
    model.save(os.path.join(root_dir,get_run_logdir()))

def plot_learning_curves(history,x_test,y_test):
    plt.plot(history.history['loss'],label='loss',color='red')
    plt.plot(history.history['val_loss'],label='val_loss',color='blue')
    plt.legend()
    #plt.gca().set_ylim(0,0.001)
    plt.show()
    score = model.evaluate(test_time_series_generator(x_test,y_test),verbose=0)
    print(score)

def main():
    data_stats(rates_frame)
    #data_visualization(rates_frame)
    x_train,x_test,y_train,y_test = data_preparation(rates_frame,y_data)
    build_model(x_train,y_train,x_test,y_test)
    #model_stats(model)
    if settings.Debug:
        plot_learning_curves(history,x_test,y_test)
        

    if settings.Debug == False:
        save_model(model)


main()




