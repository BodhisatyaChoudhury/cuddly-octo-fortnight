"""
Created on Tue Jun  9 12:41:33 2020
@author: bodhisatya choudhury
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv("Credit_Card_Applications.csv")
X= dataset.iloc[:, :-1].values
y= dataset.iloc[:, -1].values

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0, 1))
X=sc.fit_transform(X)

from minisom import MiniSom
som = MiniSom(x = 10, y = 10, input_len =15, sigma= 1.0, learning_rate=0.5)
som.random_weights_init(X)
som.train_random(data=X, num_iteration=100)

from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map().T)
colorbar()
markers = ['o','s']
colors = ['r','g']
for i, x in enumerate(X):
    w=som.winner(x)
    plot(w[0] + 0.5,
         w[1] + 0.5,
         markers[y[i]],
         markeredgecolor = colors[y[i]],
         markerfacecolor ="None",
         markersize = 10,
         markeredgewidth = 2)
show()   
             
mappings = som.win_map(X)
frauds =  np.concatenate((mappings[(8,4)], mappings[(8,6)], mappings[(5,1)], mappings[(6,4)]), axis = 0)
frauds = sc.inverse_transform(frauds)

customers = dataset.iloc[:, 1:].values
is_fraud= np.zeros(len(dataset))
for i in range(len(dataset)):
    if dataset.iloc[i, 0] in frauds:
        is_fraud[i]=1

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
customers = sc.fit_transform(customers)
import tensorflow as tf
ann=tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=2, activation='relu',))
ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
ann.fit(customers, is_fraud, batch_size = 1, epochs = 3)

y_pred = ann.predict(customers)
y_pred = np.concatenate((dataset.iloc[:, 0:1].values, y_pred), axis = 1)
y_pred = y_pred[y_pred[:, 1].argsort()]

        


