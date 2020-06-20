#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:11:40 2020

@author: Roy
"""

from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd 
from keras.callbacks import EarlyStopping


rcf_train_data = pd.read_csv('/Users/Roy/Documents/Investment/Investment_lab/Stocks/code/HMM/data/without_index_data/lstmcrfdata_5_withoutindex.csv')

rcf_train_data_ = rcf_train_data.drop([len(rcf_train_data)-1])

tag = rcf_train_data_['hidden_states'].values
rcf_train_data_ = rcf_train_data_.drop(['trade_date','ts_code','hidden_states'], axis = 1).values


x_train = rcf_train_data_.reshape((205,5,13))
y_train = tag.reshape((205,5))
y_train = [to_categorical(i, num_classes=5) for i in y_train]


X_tr, X_te, y_tr, y_te = train_test_split(x_train, y_train, test_size=0.1)




import json
import numpy as np
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_accuracy, crf_viterbi_accuracy
from keras.models import Model, Input
from keras.layers import Dense, Bidirectional, Dropout, LSTM, TimeDistributed, Masking
from keras.utils import to_categorical, plot_model
import matplotlib.pyplot as plt




def build_model(date_length, n_tags):
    # Bert Embeddings
    inputs = Input(shape=(date_length,13, ), name="data_input")
    # LSTM model
    lstm = LSTM(units=64, return_sequences=True, recurrent_dropout=0.1, name = 'LSTM')(inputs)
    drop = Dropout(0.1, name="dropout")(lstm)
    dense = TimeDistributed(Dense(n_tags, activation="softmax"), name="time_distributed")(drop)
    crf = CRF(n_tags, name = 'CRF')
    out = crf(dense)
    model = Model(inputs=inputs, outputs=out)
    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.compile(loss=crf.loss_function, optimizer='adam', metrics=[crf.accuracy])

    # 模型结构总结
    model.summary()

    return model


model = build_model(5,5)

callbacks = [EarlyStopping(monitor = 'val_loss',patience = 3,min_delta=1e-3)]
history = model.fit(X_tr, np.array(y_tr), batch_size=32, epochs=200,
                    callbacks = callbacks,
                    validation_split=0.1,
                    validation_data = (X_te, np.array(y_te)),
                    verbose=1)


y = np.argmax(model.predict(x_train), axis=2)





    




