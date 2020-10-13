#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:57:41 2020

@author: Roy
"""

import pandas as pd
import logging
import traceback
import numpy as np
from sqlalchemy import create_engine
from multiprocessing import cpu_count
from multiprocessing import Pool
import time
import os
import math
import numpy as np

import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder,OneHotEncoder



data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_variables_1'

conn = create_engine(data_base_address, encoding ='utf8')
cur = conn.execute('''SHOW TABLES''')
tables_name = cur.fetchall()

sql_cmd = "SELECT * FROM `" + tables_name[0][0] + '`;'
daily_price = pd.read_sql(sql = sql_cmd, con = conn)


sql_cmd = "SELECT * FROM `000001.sz`;"
daily_price = pd.read_sql(sql = sql_cmd, con = conn)
              







data_ = daily_price[4:]
data_ = data_.fillna(0)
data_ = data_.reset_index(drop = True)


print(data_[data_.isnull().T.any()])

dataX = []
dataY = list(data_[4:]['label'])


columns = list(data_.columns)
columns.remove('label')

for i in range(5, len(data_) + 1):
    dataX.append(data_[i-5:i][columns].values)

X = np.reshape(dataX, (len(dataX), 5, 92))



y = []

for label in dataY:
    if label == 1:
        y.append(1)
    elif label == 0:
        y.append(-1)
    else:
        y.append(0)

## 对数据集的标签数据进行编码
le = LabelEncoder()
y = le.fit_transform(y).reshape(-1,1)
ohe = OneHotEncoder()
y = ohe.fit_transform(y).toarray()



model = Sequential()
model.add(LSTM(32, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy',      optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=5, batch_size=1, verbose=1)
print(model.summary())

# summarize performance of the model
scores = model.evaluate(X, train_y, verbose=0)
print("Model Accuracy: %.2f%%" % (scores[1]*100))




import re
import pandas as pd
import numpy as np
import yaml
import tensorflow as tf
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding,multiply,GlobalAveragePooling1D,TimeDistributed,BatchNormalization,Bidirectional
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.callbacks import EarlyStopping
from keras import regularizers
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from keras.models import model_from_yaml
from keras.layers.core import *
from keras.models import *
from codecs import open
import time
from keras.models import load_model
import keras 



def model(train_X, train_y, reg_w):

    inputs = Input(name='inputs',shape =[train_X.shape[1], train_X.shape[2]])

    timedistributed = TimeDistributed(Dense(64,activation="sigmoid",name="FC1"),name = 'TimeDistributed_1')(inputs)

    LSTM_1 = LSTM(128, recurrent_dropout = 0.5, return_sequences = True, name = 'LSTM_1')(timedistributed)
    LSTM_2 = LSTM(64, recurrent_dropout = 0.5, name = 'LSTM_2')(LSTM_1)

    dropout_1 = Dropout(0.5, name = 'Dropout_1')(LSTM_2)
    FC_1 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
    BN_1 = BatchNormalization()(FC_1)
    AC_1 = Activation('sigmoid',name = 'Activation_1')(BN_1)
   
    outputs = Dense(train_y.shape[1],activation="softmax",name="msg_category")(AC_1)
    
    model = Model(inputs=inputs,outputs=outputs)
    
    return model


train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2)
train_X, val_X, train_y, val_y = train_test_split(train_X, train_y, test_size = 0.2)

reg_w = 1e-4
m = model(train_X, train_y, reg_w)
m.compile(loss="categorical_crossentropy",optimizer='adam',metrics=[keras.metrics.Recall()])
print(m.summary())



    
#train
m.fit(train_X, train_y, batch_size=32, epochs=15, validation_data=(val_X,val_y),
      callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)])


# =============================================================================
# # meta predict
# =============================================================================
meta_predict_prob = m.predict(val_X)
meta_predict = np.argmax(meta_predict_prob,axis = 1)

meta_predict = ohe.transform(meta_predict).toarray()




def meta_model(train_X, meta_y,train_y, reg_w):

    inputs = Input(name='inputs',shape =[train_X.shape[1], train_X.shape[2]])

    timedistributed = TimeDistributed(Dense(64,activation="sigmoid",name="FC1"),name = 'TimeDistributed_1')(inputs)

    LSTM_1 = LSTM(128, recurrent_dropout = 0.5, return_sequences = True, name = 'LSTM_1')(timedistributed)
    LSTM_2 = LSTM(64, recurrent_dropout = 0.5, name = 'LSTM_2')(LSTM_1)

    dropout_1 = Dropout(0.5, name = 'Dropout_1')(LSTM_2)
    FC_1 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
    BN_1 = BatchNormalization()(FC_1)
    AC_1 = Activation('sigmoid',name = 'Activation_1')(BN_1)
   
    FC_2 = Dense(10,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
    FC_2_meta = keras.layers.Concatenate(axis = -1, name = 'mate label concat')([FC_2,meta_y])
    AC_1 = Activation('sigmoid',name = 'Activation_1')(FC_2_meta)    
    
    
    outputs = Dense(train_y.shape[1],activation="softmax",name="msg_category")(AC_1)
    
    model = Model(inputs=inputs,outputs=outputs)
    
    return model

# train
    
reg_w = 1e-4
m = meta_model(val_X, meta_predict, val_y, reg_w)
m.compile(loss="categorical_crossentropy",optimizer='adam',metrics=[keras.metrics.Precision()])
print(m.summary())

m.fit(val_X, meta_predict, val_y, batch_size=32, epochs=15)

# predict
test_pre =  m.predict(train_X)

y_pre = np.argmax(test_pre,axis = 1)

y_true = np.argmax(train_y,axis = 1)


from sklearn.metrics import confusion_matrix
from sklearn import metrics

metrics.accuracy_score(y_true, y_pre)






