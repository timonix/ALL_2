from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense


...
# load the dataset
dataset = loadtxt('data/t_0.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:, 0:8]
y = dataset[:, 8]

print(X)