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

SEQUENCE_LENGTH = 100 # the length of all sequences (number of words per sample)
EMBEDDING_SIZE = 100  # Using 100-Dimensional GloVe embedding vectors
TEST_SIZE = 0.25 # ratio of testing set

BATCH_SIZE = 64
EPOCHS = 10 # number of epochs

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
    embedding_matrix = get_embedding_vectors(tokenizer)
    print("Starting...",len(tokenizer.word_index))
    model = Sequential()
    model.add(Embedding(len(tokenizer.word_index) + 1,
                        EMBEDDING_SIZE,
                        weights=[embedding_matrix],
                        trainable=False,
                        input_length=SEQUENCE_LENGTH))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(5, activation="softmax"))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])

    model.fit(X, y, epochs=20, verbose=1, validation_data=(X_test, y_test), batch_size=128)
    #print("saving")
    #model.save('cnn_model.h5')
    #model.summary()

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

    accuracy_list = [acc,precsn,recall,f1score]

    '''bars = ('Accuracy', 'Precision', 'Recall', 'F1_Score')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, accuracy_list, color=['red', 'green', 'blue', 'orange'])
    plt.xticks(y_pos, bars)
    plt.xlabel('Performance Metrics')
    plt.ylabel('Scores')
    plt.title('DL Model Evaluation')
    plt.savefig('static/accuracy.png')
    plt.clf()'''


    return acc, precsn, recall, f1score


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

# get the loss and metrics
#result = model.evaluate(X_test, y_test)
# extract those
#loss = result[0]
#accuracy = result[1]
#precision = result[2]
#recall = result[3]

#print(f"[+] Accuracy: {accuracy*100:.2f}%")
#print("Model created")

'''def get_predictions(text):
    sequence = tokenizer.texts_to_sequences([text])
    # pad the sequence
    sequence = pad_sequences(sequence, maxlen=SEQUENCE_LENGTH)
    # get the prediction
    prediction = model.predict(sequence)[0]
    # one-hot encoded vector, revert using np.argmax
    return int2label[np.argmax(prediction)]

text = "Need a loan? We offer quick and easy approval. Apply now for cash in minutes!."
print(get_predictions(text))'''

if __name__ == '__main__':
    dl_evaluation_process()