import numpy as np
from keras.models import Sequential,Model
from keras.layers import Flatten, Bidirectional, Dense, Dropout, Conv1D, Conv2D, concatenate, Input, add, MaxPool1D, GlobalMaxPool1D, LSTM, Embedding
from keras.layers import Flatten, Dense, Embedding, concatenate, Input, Dropout, LSTM, Average, Bidirectional, Conv1D, GlobalMaxPooling1D, GlobalAveragePooling1D, BatchNormalization, Conv2D, GlobalAveragePooling2D
import matplotlib.pyplot as plt
import random
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# get 6000 sequence data which has 200 Nucleotides in the beginning of original RNA and 200 in the end
train = np.load('200x_y200.npz')
train_negative = np.load("200x_y200_negative.npz")
x_positive = train['x_all']
x_negative = train_negative["x_all_negative"]
x_all = np.vstack((x_positive, x_negative))

# label the data : 1 for the exo and 0 for the nonexo
y_all = np.hstack((np.ones(6000), np.zeros(6000)))

# shuffle the 6000 data to improve the accuracy of classification
index = [i for i in range(len(x_all))]
random.shuffle(index)
x_all = x_all[index]
y_all = y_all[index]

# 3 basic neural network models

'''
# FNN  0.7775     0.4690
model = Sequential()
model.add(Flatten(input_shape=(400, 4)))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(x_all, y_all, batch_size=256, epochs=80, validation_split=0.2)
model.summary()
'''


# CNN  0.9908    0.0210
input = Input(shape=(400, 4))
Conv1 = Conv1D(10, 3, padding='same')(input)
Conv2 = Conv1D(10, 5, padding='same')(input)
merge = concatenate([Conv1, Conv2], axis=1)
x = Conv1D(20, 3, padding='same')(merge)
x = MaxPool1D(5)(x)
x = Flatten()(x)
x = Dropout(0.5)(x)
x = Dense(32, activation='relu')(x)
x = Dense(1, activation='sigmoid')(x)
model = Model(input,x)
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
history = model.fit(x_all, y_all, 256, epochs=50, validation_split=0.2)
model.summary()


'''
# LSTM  0.9917   0.0263
model = Sequential()
model.add(Bidirectional(LSTM(64),input_shape = (400, 4)))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy',metrics=['acc'])
history = model.fit(x_all, y_all, batch_size=32, epochs=80, validation_split=0.2)
model.summary()
'''
'''
# CNN-LSTM not better than CNN for this task
input = Input(shape=(400, 4))
Conv1 = Conv1D(10, 3, padding='same')(input)
Conv2 = Conv1D(10, 5, padding='same')(input)
merge = concatenate([Conv1, Conv2], axis=1)
x = Conv1D(20, 3, padding='same')(merge)
x = MaxPool1D(5)(x)
x = Bidirectional(LSTM(64))(x)
x = Dropout(0.5)(x)
x = Dense(32, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(1, activation='sigmoid')(x)
model = Model(input, x)
model.compile(optimizer='adam', loss='binary_crossentropy',metrics=['acc'])
history = model.fit(x_all, y_all, batch_size=32, epochs=80, validation_split=0.2)
model.summary()
'''

# figure for models loss
fig1 = plt.figure(5)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['Training', 'Validation'])
plt.show(fig1)

# figure for models accuracy
fig2 = plt.figure(6)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Training', 'Validation'])
plt.show(fig2)

