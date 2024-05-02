import time
import pickle
import tensorflow as tf
import pandas as pd
import tqdm
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn.model_selection import train_test_split
#from tensorflow.keras.layers import Embedding, Dropout, Dense
from tensorflow.keras.models import Sequential
#from tensorflow.keras.metrics import Recall, Precision



from sklearn.metrics import f1_score, precision_score, accuracy_score, recall_score

from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D, Dropout, Dense, Input, Embedding, MaxPooling1D, Flatten

SEQUENCE_LENGTH = 500 # the length of all sequences (number of words per sample)
EMBEDDING_SIZE = 100  # Using 100-Dimensional GloVe embedding vectors
TEST_SIZE = 0.25 # ratio of testing set

BATCH_SIZE = 64
EPOCHS = 10 # number of epochs

maxlen = 80
batch_size = 32

label2int = {"frustrated": 0, "negative": 1,"neutral":2,"positive":3,"satisfied":4}

int2label = {0: "frustrated", 1: "negative",2:"neutral",3:"positive",4:"satisfied"}

def load_data():
    """
    Loads SMS Spam Collection dataset
    """
    data = pd.read_csv("train.csv",encoding='latin-1')

    texts = data['feedback'].values

    labels=data['sentiment'].values


    return texts, labels

def dl_evaluation_process():
    print("loading data")
    X, y = load_data()

    # Text tokenization
    # vectorizing text, turning each text into sequence of integers
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X)
    # lets dump it to a file, so we can use it in testing
    pickle.dump(tokenizer, open("tokenizer.pickle", "wb"))
    # convert to sequence of integers
    X = tokenizer.texts_to_sequences(X)

    # convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    # pad sequences at the beginning of each sequence with 0's
    # for example if SEQUENCE_LENGTH=4:
    # [[5, 3, 2], [5, 1, 2, 3], [3, 4]]
    # will be transformed to:
    # [[0, 5, 3, 2], [5, 1, 2, 3], [0, 0, 3, 4]]
    X = pad_sequences(X, maxlen=SEQUENCE_LENGTH)

    # One Hot encoding labels
    # [spam, ham, spam, ham, ham] will be converted to:
    # [1, 0, 1, 0, 1] and then to:
    # [[0, 1], [1, 0], [0, 1], [1, 0], [0, 1]]

    y = [label2int[label] for label in y]
    y = to_categorical(y)

    # split and shuffle
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=7)
    # print our data shapes
    '''print("X_train.shape:", X_train.shape)
    print("X_test.shape:", X_test.shape)
    print("y_train.shape:", y_train.shape)
    print("y_test.shape:", y_test.shape)'''

    #print("EMD Matrix")

    print("Starting...")
    # Define the model
    print('Build model...')
    model = Sequential()
    model.add(Flatten(input_shape=(500,)))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(5, activation='softmax'))

    # Compile the model
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # Train the model
    print('Train...')
    model.fit(X, y,
              batch_size=batch_size,
              epochs=20,
              validation_data=(X_test, y_test))

    y_test = np.argmax(y_test, axis=1)
    y_pred = np.argmax(model.predict(X_test), axis=1)

    acc = accuracy_score(y_test, y_pred) * 100

    precsn = precision_score(y_test, y_pred, average="macro") * 100

    recall = recall_score(y_test, y_pred, average="macro") * 100

    f1score = f1_score(y_test, y_pred, average="macro") * 100

    print("acc=", acc)

    print("precsn=", precsn)

    print("recall=", recall)

    print("f1score=", f1score)




    return acc, precsn, recall, f1score

if __name__ == '__main__':
  dl_evaluation_process()