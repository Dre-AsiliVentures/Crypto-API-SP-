#!/usr/bin/env python
# coding: utf-8

# # LSTM PRICE PREDICTION MODEL (Stock)

# Procedure
# 1. Collect stock data
# 2. Pre-process data (Training & Testing)
# 3. Create a LSTM Stacked Model
# 4. Future Price Predicton (30-days) & Output plots

# In[6]:


#pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.8.0-py3-none-any.whl')
#pip3 install --user --upgrade tensorflow  # install in $HOME')
#get_ipython().system('pip install pandas-datareader')
#get_ipython().system('https://www.youtube.com/watch?v=H6du_pfuznE')


# In[7]:


import os
import pandas as pd
from pandas.errors import EmptyDataError
import pandas_datareader as pdr
import matplotlib.pyplot as plt


# In[8]:


#API_KEY =os.environ.get('TIINGO_API_KEY')
API_KEY=''
df=pdr.get_data_tiingo('AAPL',api_key=API_KEY)
df.to_csv('AAPL.csv')
try:
    df=pd.read_csv('AAPL.csv')
except EmptyDataError:
    pass
df1=df.reset_index()['close'] # Extract the close column for price prediction
df1
plt.plot(df1)


# In[9]:


df1[1260:]
#print(df.tail())


# # LSTM Price Prediction 
# 

# In[10]:


from sklearn.preprocessing import MinMaxScaler
import numpy as np
import math
from sklearn.metrics import mean_squared_error
scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
print(df1)


# In[11]:


# Splitting of dataset into train-test split
training_size=int(len(df1)*0.65)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]


# In[12]:


training_size,test_size


# In[13]:


train_data


# In[14]:


import numpy
def create_dataset(dataset,time_step=1):
    dataX,dataY=[],[]
    for i in range(len(dataset)-time_step-1):
        a=dataset[i:(i+time_step),0]
        dataX.append(a)
        dataY.append(dataset[i+time_step,0])
    return numpy.array(dataX),numpy.array(dataY)

# reshape into X=t, t+1, t+2, t+3 and Y=t+4
time_step=100
X_train,y_train=create_dataset(train_data,time_step)
X_test,y_test=create_dataset(test_data,time_step)
print(X_train.shape),print(y_train.shape)


# In[15]:


print(X_test.shape),print(y_test.shape)


# # Stacked LSTM Model

# In[1]:


from tensorflow import keras
from keras.models import *
from keras.layers import *


# In[ ]:


model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')


# model.summary()

# In[ ]:


model.summary()


# In[ ]:


model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=100,batch_size=64,verbose=1)


# In[5]:


import tensorflow
tensorflow.__version__


# In[21]:


tensorflow.__version__


# # Tensorflow Predictions

# In[ ]:


train_predict=model.predict(X_train)
test_predict=model.predict(X_test)


# In[ ]:


# Transform back to the original form
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)


# In[ ]:


# Calculate the model metrics
math.sqrt(mean_squared_error(y_train,train_predict))


# In[ ]:


# Plotting
# Shifting train predictions for plotting
look_back=100
trainPredictPlot=numpy.empty_like(df1)
trainPredictPlot[:,:]=np.nan
trainPredictPlot[look_back:len(train_predict)+look_back,:]=train_predict

# Shift the Test Predictions for plotting
testPredictPlot=numpy.empty_like(df1)
testPredictPlot[:,:]=numpy.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1, :] = test_predict

# Plot the baseline and Predictions
plt.plot(scaler.inverse_transform(df1))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()


# In[ ]:


len(test_data)


# In[ ]:


x_input=test_data[341:].reshape(1,-1)
x_input.shape


# In[ ]:


temp_input=list(x_input)
temp_input=temp_input[0].tolist()
temp_input


# In[ ]:


# Predictions for the Next 10 days
from numpy import array
lst_output=[]
n_steps=100
i=0
while(i<30):
    if(len(temp_input)>100):
        x_input=np.array(temp_input[1:1])
        print("{} day input {}".format(i,x_input))
        x_input=x_input.reshape(1,-1)
        x_input=x_input.reshape((1,n_steps,1))
        yhat=model.predict(x_input,verbose=0)
        print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat[0].tolist())
        temp_input=temp_input[1:]
        
        #print temp input
        lst_output.extend(yhat.tolist())
        i=i+1
    else:
        x_input=x_input.reshape((1,n_steps,1))
        yhat=model.predict(x_input,verbose=0)
        print(yhat[0])
        temp_input.extend(yhat[0].tolist())
        print(len(temp_input))
        lst_output.extend(yhat.tolist())
        i=i+1
print(lst_output)


# In[ ]:


day_new=np.arrange(1,101)
day_pred=np.arrange(101,131)


# In[ ]:


len(df1)


# In[ ]:


plt.plot(day_new,scaler.inverse_transform(df1[1158:]))
plt.plot(day_pred,scaler.inverse_transform(lst_output))


# In[ ]:


df3=df1.df1.tolist()
df3.extend(lst_output)
plt.plot(df3[1200:])


# In[ ]:


df3.scalerinverse_transform(df3).tolist()
df3


# In[ ]:


plt.plot(df3)

