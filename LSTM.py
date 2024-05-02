import time
import pickle
import tensorflow as tf
import pandas as pd
import tqdm
import numpy as np
import os
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
from keras.models import load_model

from sklearn.metrics import f1_score, precision_score, accuracy_score, recall_score

from tensorflow.keras.layers import LSTM, GlobalMaxPooling1D, Dropout, Dense, Input, Embedding, MaxPooling1D, Flatten,BatchNormalization

SEQUENCE_LENGTH = 100 # the length of all sequences (number of words per sample)
EMBEDDING_SIZE = 100  # Using 100-Dimensional GloVe embedding vectors
TEST_SIZE = 0.25 # ratio of testing set

BATCH_SIZE = 64
EPOCHS = 20 # number of epochs

label2int = {"frustrated": 0, "negative": 1,"neutral":2,"positive":3,"satisfied":4}

int2label = {0: "frustrated", 1: "negative",2:"neutral",3:"positive",4:"satisfied"}


     




def get_embedding_vectors(tokenizer, dim=100):
    embedding_index = {}
    with open(f"data/glove.6B.{dim}d.txt", encoding='utf8') as f:
        for line in tqdm.tqdm(f, "Reading GloVe"):
            values = line.split()
            word = values[0]
            vectors = np.asarray(values[1:], dtype='float32')
            embedding_index[word] = vectors

    word_index = tokenizer.word_index
    embedding_matrix = np.zeros((len(word_index) + 1, dim))
    for word, i in word_index.items():
        embedding_vector = embedding_index.get(word)
        if embedding_vector is not None:
            # words not found will be 0s
            embedding_matrix[i] = embedding_vector

    return embedding_matrix



def get_predictions(text):
    tokenizer = Tokenizer()
    
    model_path = 'lstm_model.h5'
    model = load_model(model_path)
    sequence = tokenizer.texts_to_sequences(text)
    # pad the sequence
    sequence = pad_sequences(sequence, maxlen=SEQUENCE_LENGTH)
    # get the prediction
    prediction = model.predict(sequence)

    res=[]

    for p1 in prediction:
        res.append(int2label[np.argmax(p1)])
    return res

if __name__ == '__main__':
    t=[' Sooo SAD I will miss you here in San Diego!!!', 'Stolen iPhone 15 pro', 'iPhone 15 Pro and iPhone 15 Pro Max Feature Increased 8GB of RAM', 'Apple announces iPhone 15 Pro and Pro Max', 'Temperature of my iPhone 15 Pro Max while on the phone for 5 mins.', 'I traded in my iPhone 14 Pro for the iPhone 15 Pro Max, then FedEx lost the old phone', 'iPhone 15 Pro Max crushes Google Pixel 8 Pro in speed test', 'Apple Design Team Making The New iPhone 15 Pro Max', 'iPhone 15 Pro Could Be Most Lightweight Pro Model Since iPhone XS', ' iPhone 15 Pro/Pro Max is so sad']
    print(get_predictions(t))
    
