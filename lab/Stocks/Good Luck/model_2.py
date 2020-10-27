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
# =============================================================================
#  import data
# =============================================================================
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_variables_1'
conn = create_engine(data_base_address, encoding ='utf8')
cur = conn.execute('''SHOW TABLES''')
tables_name = cur.fetchall()

train_X = []
val_X = []
test_X = []

train_Y = []
val_Y = []
test_Y = []

t = 0
for table in tables_name:

    t += 1
    print(t)
    
    sql_cmd = "SELECT * FROM `" + table[0] + '`;'
    variable = pd.read_sql(sql = sql_cmd, con = conn)
    
    variable = variable[4:]
    variable = variable.fillna(0)
    
    variable.set_index('trade_date',inplace=True)
    
    variable_train = variable['2011':'2016']
    variable_val = variable['2017':'2018']
    variable_test = variable['2019']
    # train set
    for i in range(10, len(variable_train) + 1):
        if variable_train.iloc[i-1]['open'] >= 20:
            continue
        else:
            train_Y.append(variable_train.iloc[i-1]['label'])
            columns = list(variable_train.columns)
            remove = ['label','open','high','low','close']
            columns = [x for x in columns if x not in remove]
            train_X.append(variable_train[i-10:i][columns].values)
    # val test
    for i in range(10, len(variable_val) + 1):
        if variable_val.iloc[i-1]['open'] >= 20:
            continue
        else:
            val_Y.append(variable_val.iloc[i-1]['label'])
            columns = list(variable_val.columns)
            remove = ['label','open','high','low','close']
            columns = [x for x in columns if x not in remove]
            val_X.append(variable_val[i-10:i][columns].values)
    # test set  
    for i in range(10, len(variable_test) + 1):
        if variable_test.iloc[i-1]['open'] >= 20:
            continue
        else:
            test_Y.append(variable_test.iloc[i-1]['label'])
            columns = list(variable_test.columns)
            remove = ['label','open','high','low','close']
            columns = [x for x in columns if x not in remove]
            test_X.append(variable_test[i-10:i][columns].values)
    
    
    
    
    
    
dataX = []
dataY = list(data_[9:]['label'])


columns = list(data_.columns)
columns.remove('label')

for i in range(10, len(data_) + 1):
    dataX.append(data_[i-10:i][columns].values)

X = np.reshape(dataX, (len(dataX), 10, 92))

    
    

selected_data = all_data[all_data['open'] < 20]
train_X = selected_data['2011':'2016']
val_X = selected_data['2017':'2018']
test_X = selected_data['2019']

                  
all_data.set_index('trade_date',inplace=True)

all_data['label_dummy'] = all_data['label'].apply(lambda x: x if x == 1 else (-1 if x == 0 else 0))








dataX = []
dataY = list(data_[9:]['label'])


columns = list(data_.columns)
columns.remove('label')

for i in range(10, len(data_) + 1):
    dataX.append(data_[i-10:i][columns].values)

X = np.reshape(dataX, (len(dataX), 10, 92))



y = []

for label in dataY:
    if label == 1:
        y.append(1)
    elif label == 0:
        y.append(-1)
    else:
        y.append(0)





# data select and train val test split

selected_data = all_data[all_data['open'] < 20]
train_X = selected_data['2011':'2016']
val_X = selected_data['2017':'2018']
test_X = selected_data['2019']

train_Y = list(train_X['label_dummy'])
val_Y = list(val_X['label_dummy'])
test_Y = list(test_X['label_dummy'])

# label y to dummy

le = LabelEncoder()
train_y= le.fit_transform(train_Y).reshape(-1,1)
ohe = OneHotEncoder()
train_y = ohe.fit_transform(train_y).toarray()

val_y = le.transform(val_Y).reshape(-1,1)
val_y = ohe.transform(val_y).toarray()

test_y = le.transform(test_Y).reshape(-1,1)
test_y = ohe.transform(test_y).toarray()

# =============================================================================
# model
# =============================================================================
# model_layer_1
def model(train_X, train_y, reg_w):

    inputs = Input(name='inputs',shape =[train_X.shape[1], train_X.shape[2]])

    LSTM_1 = LSTM(128, recurrent_dropout = 0.5, return_sequences = False, name = 'LSTM_1')(inputs)
    LSTM_2 = LSTM(64, recurrent_dropout = 0.5, name = 'LSTM_2')(LSTM_1)

    dropout_1 = Dropout(0.5, name = 'Dropout_1')(LSTM_2)
    FC_1 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
    BN_1 = BatchNormalization()(FC_1)
    AC_1 = Activation('sigmoid',name = 'Activation_1')(BN_1)
    
    dropout_2 = Dropout(0.5, name = 'Dropout_2')(AC_1)
    FC_2 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_2)
    BN_2 = BatchNormalization()(FC_2)
    AC_2 = Activation('sigmoid',name = 'Activation_1')(BN_2)
   
    outputs = Dense(train_y.shape[1],activation="softmax",name="msg_category")(AC_2)
    model = Model(inputs=inputs,outputs=outputs)

    return model


# train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.2)
# train_X, val_X, train_y, val_y = train_test_split(train_X, train_y, test_size = 0.2)

reg_w = 1e-4
model_layer_1 = model(train_X, train_y, reg_w)
model_layer_1.compile(loss="categorical_crossentropy",optimizer='adam',metrics=[keras.metrics.Recall()])
print(model_layer_1.summary())

#train
model_layer_1.fit(train_X, train_y, batch_size=1, epochs=15, validation_data=(val_X,val_y),
                  callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)])

# meta predict
meta_predict_prob = model_layer_1.predict(train_X)
meta_predict = np.argmax(meta_predict_prob,axis = 1)













'''---------------------------------------'''
# meta predict
meta_predict_prob = model_layer_1.predict(train_X)
meta_predict = np.argmax(meta_predict_prob,axis = 1)



def meta_model(train_X, meta_y,train_y, reg_w):

    inputs_x = Input(name='inputs_x',shape = [train_X.shape[1], train_X.shape[2]])
    inputs_meta_y = Input(name = 'inputs_meta_y', shape = [meta_y.shape[1]])

    # timedistributed = TimeDistributed(Dense(64,activation="sigmoid",name="FC1"),name = 'TimeDistributed_1')(inputs_x)

    LSTM_1 = LSTM(128, recurrent_dropout = 0.5, return_sequences = False, name = 'LSTM_1')(inputs_x)
    # LSTM_2 = LSTM(64, recurrent_dropout = 0.5, name = 'LSTM_2')(LSTM_1)

    dropout_1 = Dropout(0.5, name = 'Dropout_1')(LSTM_1)
    FC_1 = Dense(32,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
    BN_1 = BatchNormalization()(FC_1)
    AC_1 = Activation('sigmoid',name = 'Activation_1')(BN_1)
   
    FC_2 = Dense(10,kernel_regularizer=regularizers.l2(reg_w),name="FC1")(dropout_1)
    FC_2_meta = keras.layers.Concatenate(axis = -1, name = 'mate_label_concat')([FC_2,inputs_meta_y])
    AC_1 = Activation('sigmoid',name = 'Activation_1')(FC_2_meta)    
    
    
    outputs = Dense(train_y.shape[1],activation="softmax",name="msg_category")(AC_1)
    
    model = Model(inputs=[inputs_x, inputs_meta_y], outputs=outputs)
    
    return model

# train
    
reg_w = 1e-4
meta = meta_model(val_X, meta_predict, val_y, reg_w)
meta.compile(loss="categorical_crossentropy",optimizer='adam',metrics=[keras.metrics.Precision()])
print(m.summary())

meta.fit([val_X, meta_predict], val_y, batch_size=32, epochs=30)


# =============================================================================
# # predict
# =============================================================================
# meta predict
meta_pred_prob =  m.predict(test_X)
meta_pred = np.argmax(meta_pred_prob,axis = 1)
meta_pred = meta_pred.reshape(meta_pred.shape[0],1)
meta_predict = ohe.transform(meta_pred).toarray()

# result predict
y_pred_prob = meta.predict([test_X, meta_predict])
y_pred = np.argmax(y_pred_prob,axis = 1)
y_pred = y_pred.reshape(y_pred.shape[0],1)
y_pred = ohe.transform(y_pred).toarray()

from sklearn.metrics import confusion_matrix
from sklearn import metrics

metrics.accuracy_score(test_y, y_pred)


print(metrics.classification_report(y_true=test_y, y_pred=y_pred))

confusion_matrix(np.argmax(test_y), np.argmax(y_pred))
