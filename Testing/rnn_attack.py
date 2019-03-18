import numpy as np 
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re
import json

def get_all_data(filename,delimiter=','):
    all_data = np.genfromtxt(filename, delimiter=delimiter)
    # Randomly sample from the input file if it is for testing data
    features = all_data[:, :-1]
    labels = all_data[:, all_data.shape[1] - 1].ravel()
    return features, labels


look_back=2

# convert an array of values into a dataset matrix
def create_dataset(dataset):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 2])
	return np.array(dataX), np.array(dataY)

X, Y = get_all_data('TrainingData/ground_truth.csv')




embed_dim = 2
lstm_out = 200
batch_size= 32

##Buidling the LSTM network
outputs = to_categorical(Y).shape[1]
print(outputs)

model = Sequential()
model.add(Embedding(X.shape[0], embed_dim,input_length = X.shape[1], dropout = 0.2))
model.add(LSTM(lstm_out))
model.add(Dense(10,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])


X_train, X_valid, Y_train, Y_valid = train_test_split(X,to_categorical(Y), test_size = 0.20, random_state = 42)

#Here we train the Network.
print(X_train.shape)
model.fit(X_train, Y_train, batch_size = batch_size, epochs = 5,  verbose = 1)

# Measuring score and accuracy on validation set

score,acc = model.evaluate(X_valid, Y_valid, verbose = 2, batch_size = batch_size)
print("Logloss score: %.2f" % (score))
print("Validation set Accuracy: %.2f" % (acc))