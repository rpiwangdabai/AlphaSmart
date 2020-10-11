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


sql_cmd = "SELECT * FROM `000001`;"
daily_price = pd.read_sql(sql = sql_cmd, con = conn)
              


X = np.reshape(daily_price, (5, 5, 93))



# prepare the dataset of input to output pairs encoded as integers
seq_length = 1
dataX = []
dataY = []
for i in range(0, len(alphabet) - seq_length, 1):
    seq_in = alphabet[i:i + seq_length]
    seq_out = alphabet[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
    print (seq_in, '->', seq_out)

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
train_y = le.fit_transform(y).reshape(-1,1)
ohe = OneHotEncoder()
train_y = ohe.fit_transform(train_y).toarray()



model = Sequential()
model.add(LSTM(32, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(train_y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy',      optimizer='adam', metrics=['accuracy'])
model.fit(X, train_y, epochs=5, batch_size=1, verbose=1)


# summarize performance of the model
scores = model.evaluate(X, train_y, verbose=0)
print("Model Accuracy: %.2f%%" % (scores[1]*100))




















