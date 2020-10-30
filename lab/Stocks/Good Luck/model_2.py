# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:26:23 2020

@author: Lenovo
"""

import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding,multiply,GlobalAveragePooling1D,TimeDistributed,BatchNormalization,Bidirectional
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.callbacks import EarlyStopping
from keras import regularizers
from sklearn.model_selection import train_test_split
import keras 
from sqlalchemy import create_engine
from sklearn.utils import shuffle
from matplotlib import pyplot
import random
# =============================================================================
#  import data
# =============================================================================
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_variables_1'
conn = create_engine(data_base_address, encoding ='utf8')
cur = conn.execute('''SHOW TABLES''')
tables_name = cur.fetchall()
random.shuffle(tables_name)

tables_name_ = tables_name

train_X = []
val_X = []
test_X = []

train_Y = []
val_Y = []
test_Y = []



# remove_1 = [x for x in a if 'z_value' in x ]
remove_1 = []
remove_2 = ['label','open','high','low','close']
remove = remove_1 + remove_2

t = 0
for table in tables_name_:

    t += 1
    print(t)
    
    sql_cmd = "SELECT * FROM `" + table[0] + '`;'
    variable = pd.read_sql(sql = sql_cmd, con = conn)
    
    # do not consider stocks which ipo with in 3 month, 60 trading days
    
    if len(variable) < 60:
        continue
    variable = variable[30:]
    variable = variable.fillna(0)
    
    variable.set_index('trade_date',inplace=True)
    try:
        variable_train = variable['2011':'2016']
        variable_val = variable['2017':'2018']
        variable_test = variable['2019']
    except KeyError:
        continue
    # train set
    for i in range(3, len(variable_train) + 1):
        if variable_train.iloc[i-1]['open'] >= 20:
            continue
        else:
            train_Y.append(variable_train.iloc[i-1]['label'])
            columns = list(variable_train.columns)
            columns = [x for x in columns if x not in remove]
            train_X.append(variable_train[i-3:i][columns].values)
    # val test
    for i in range(3, len(variable_val) + 1):
        if variable_val.iloc[i-1]['open'] >= 20:
            continue
        else:
            val_Y.append(variable_val.iloc[i-1]['label'])
            columns = list(variable_val.columns)
            columns = [x for x in columns if x not in remove]
            val_X.append(variable_val[i-3:i][columns].values)
    # test set  
    for i in range(3, len(variable_test) + 1):
        if variable_test.iloc[i-1]['open'] >= 20:
            continue
        else:
            test_Y.append(variable_test.iloc[i-1]['label'])
            columns = list(variable_test.columns)
            columns = [x for x in columns if x not in remove]
            test_X.append(variable_test[i-3:i][columns].values)
    
    

    
# data_dict = {}
# data_dict['train_X'] = train_X
# data_dict['val_X'] = val_X
# data_dict['test_X'] = test_X
# data_dict['train_Y'] = train_Y
# data_dict['val_Y'] = val_Y
# data_dict['test_Y'] = test_Y
    
# data_dict = np.load('C:/Users/Lenovo/Desktop/data_dict.npy', allow_pickle=True).item()

# train_X = data_dict['train_X']
# val_X = data_dict['val_X'] 
# test_X = data_dict['test_X']
# train_Y = data_dict['train_Y']
# val_Y = data_dict['val_Y']
# test_Y = data_dict['test_Y']


# train dataset and label transfer

train_x = np.reshape(train_X, (len(train_X), 3, 93))
val_x = np.reshape(val_X, (len(val_X), 3, 93))
test_x = np.reshape(test_X, (len(test_X), 3, 93))

for i in range(len(train_Y)):
    if train_Y[i] == 1:
        continue
    elif train_Y[i] == 0:
        train_Y[i] = -1
    else:
        train_Y[i] = 0

for i in range(len(val_Y)):
    if val_Y[i] == 1:
        continue
    elif val_Y[i] == 0:
        val_Y[i] = -1
    else:
        val_Y[i] = 0

for i in range(len(test_Y)):
    if test_Y[i] == 1:
        continue
    elif test_Y[i] == 0:
        test_Y[i] = -1
    else:
        test_Y[i] = 0





# label y to dummy

le = LabelEncoder()
le.fit(train_Y)
train_y= le.transform(train_Y).reshape(-1,1)
ohe = OneHotEncoder()
ohe.fit(train_y)
train_y_oh = ohe.transform(train_y).toarray()

val_y = le.transform(val_Y).reshape(-1,1)
val_y_oh = ohe.transform(val_y).toarray()

test_y = le.transform(test_Y).reshape(-1,1)
test_y_oh = ohe.transform(test_y).toarray()


# shuffle


train_x, train_y = shuffle(train_x, train_y, random_state=0)
val_x, val_y = shuffle(val_x, val_y, random_state=0)
test_x, test_y = shuffle(test_x, test_y, random_state=0)


# =============================================================================
# model
# =============================================================================
# model_layer_1
def model(train_X, train_y, reg_w):

    inputs = Input(name='inputs',shape =[train_X.shape[1], train_X.shape[2]])

    LSTM_1 = LSTM(128, recurrent_dropout = 0.5, return_sequences = False, name = 'LSTM_1')(inputs)
    # LSTM_2 = LSTM(64, recurrent_dropout = 0.5, name = 'LSTM_2')(LSTM_1)

    dropout_1 = Dropout(0.5, name = 'Dropout_1')(LSTM_1)
    FC_1 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
    BN_1 = BatchNormalization()(FC_1)
    AC_1 = Activation('sigmoid',name = 'Activation_1')(BN_1)
    
    # dropout_2 = Dropout(0.5, name = 'Dropout_2')(AC_1)
    # FC_2 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC2")(dropout_2)
    # BN_2 = BatchNormalization()(FC_2)
    # AC_2 = Activation('sigmoid',name = 'Activation_2')(BN_2)
   
    outputs = Dense(train_y.shape[1],activation="softmax",name="msg_category")(AC_1)
    model = Model(inputs=inputs,outputs=outputs)

    return model


# train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2)
# train_X, val_X, train_y, val_y = train_test_split(train_X, train_y, test_size = 0.2)

reg_w = 1e-4
model_layer_1 = model(train_x, train_y_oh, reg_w)
model_layer_1.compile(loss="categorical_crossentropy",optimizer='adam',metrics=['accuracy'])
print(model_layer_1.summary())

#train
history = model_layer_1.fit(train_x, train_y_oh, batch_size=256, epochs=10, validation_data=(val_x,val_y_oh),
                  callbacks=[EarlyStopping(monitor='val_loss',patience=50)])

#plot loss
_, train_acc = model_layer_1.evaluate(train_x, train_y_oh, verbose=0)
_, test_acc = model_layer_1.evaluate(test_x, test_y_oh, verbose=0)
print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))
# plot training history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()


# # meta predict
# meta_predict_prob = model_layer_1.predict(train_X)
# meta_predict = np.argmax(meta_predict_prob,axis = 1)













# '''---------------------------------------'''
# # meta predict
# meta_predict_prob = model_layer_1.predict(train_X)
# meta_predict = np.argmax(meta_predict_prob,axis = 1)



# def meta_model(train_X, meta_y,train_y, reg_w):

#     inputs_x = Input(name='inputs_x',shape = [train_X.shape[1], train_X.shape[2]])
#     inputs_meta_y = Input(name = 'inputs_meta_y', shape = [meta_y.shape[1]])

#     # timedistributed = TimeDistributed(Dense(64,activation="sigmoid",name="FC1"),name = 'TimeDistributed_1')(inputs_x)

#     LSTM_1 = LSTM(128, recurrent_dropout = 0.5, return_sequences = False, name = 'LSTM_1')(inputs_x)
#     # LSTM_2 = LSTM(64, recurrent_dropout = 0.5, name = 'LSTM_2')(LSTM_1)

#     dropout_1 = Dropout(0.5, name = 'Dropout_1')(LSTM_1)
#     FC_1 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
#     BN_1 = BatchNormalization()(FC_1)
#     AC_1 = Activation('sigmoid',name = 'Activation_1')(BN_1)
   
#     FC_2 = Dense(10,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
#     FC_2_meta = keras.layers.Concatenate(axis = -1, name = 'mate_label_concat')([FC_2,inputs_meta_y])
#     AC_1 = Activation('sigmoid',name = 'Activation_1')(FC_2_meta)    
    
    
#     outputs = Dense(train_y.shape[1],activation="softmax",name="msg_category")(AC_1)
    
#     model = Model(inputs=[inputs_x, inputs_meta_y], outputs=outputs)
    
#     return model

# # train
    
# reg_w = 1e-4
# meta = meta_model(val_X, meta_predict, val_y, reg_w)
# meta.compile(loss="categorical_crossentropy",optimizer='adam',metrics=[keras.metrics.Precision()])
# print(m.summary())

# meta.fit([val_X, meta_predict], val_y, batch_size=32, epochs=30)


# # =============================================================================
# # # predict
# # =============================================================================
# # meta predict
# meta_pred_prob =  m.predict(test_X)
# meta_pred = np.argmax(meta_pred_prob,axis = 1)
# meta_pred = meta_pred.reshape(meta_pred.shape[0],1)
# meta_predict = ohe.transform(meta_pred).toarray()

# # result predict
# y_pred_prob = meta.predict([test_X, meta_predict])
# y_pred = np.argmax(y_pred_prob,axis = 1)
# y_pred = y_pred.reshape(y_pred.shape[0],1)
# y_pred = ohe.transform(y_pred).toarray()

# from sklearn.metrics import confusion_matrix
# from sklearn import metrics

# metrics.accuracy_score(test_y, y_pred)


# print(metrics.classification_report(y_true=test_y, y_pred=y_pred))

# confusion_matrix(np.argmax(test_y), np.argmax(y_pred))
