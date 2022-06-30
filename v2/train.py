import numpy as np
import csv
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow import keras
import tensorflow.keras.callbacks as carl
import representation

# to measure exec time
from timeit import default_timer as timer   

TESTING_SIZE = 1000
EPOCHS = 1000
BATCH_SIZE = 100
DATASET = "../datasets/chessData-small.csv"

def create_model():
    model = Sequential()
    model.add(Dense(64, input_dim=453, activation='tanh'))
    model.add(Dense(32, activation='tanh'))
    model.add(Dense(16, activation='tanh'))
    model.add(Dense(16, activation='tanh'))
    model.add(Dense(4, activation='tanh'))
    model.add(Dense(4, activation='tanh'))
    model.add(Dense(1, activation='tanh'))
    # compile the keras model
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model

def train(model):
    print("start")
    starttime = timer()

    with open(DATASET, newline='') as csvfile:
        dataset = list(csv.reader(csvfile))
    dataset = dataset[1:] # remove column names
    print("data loaded at", timer() - starttime)

    flatBoards = []
    groundEvaluations = []

    for n in range(len(dataset)):
        fen = dataset[n][0]
        groundEvaluation = dataset[n][1]

        board, extraInfo = representation.evaluateFenIntoBoard(fen)
        if groundEvaluation[0] == "#":  # if evaluation is mate in...
            if groundEvaluation[1] == "+": # if mate in ... is to black
                groundEvaluation = "2000"
            else:
                groundEvaluation = "-2000"
        if extraInfo == {}: # invalid FEN
            continue
        flatBoard = representation.flattenBoard(board, extraInfo)
        flatBoards.append(flatBoard)
        groundEvaluation2 = max(-1, min(1, float(groundEvaluation) / 2000))
        groundEvaluations.append(groundEvaluation2) # clamp groundEvaluation to +/-1000 and normalise to 0-1

    del dataset

    xTrain = flatBoards[:-TESTING_SIZE]
    yTrain = groundEvaluations[:-TESTING_SIZE]

    xTest = flatBoards[-TESTING_SIZE:]
    yTest = groundEvaluations[-TESTING_SIZE:]

    print("FENs cleaned & flattened at", timer() - starttime)
    print("number of valid flatboards", len(flatBoards))

    del flatBoards
    del groundEvaluations

    # Create a callback that saves the model's weights every 5 epochs
    cp_callback = keras.callbacks.ModelCheckpoint(
        filepath="./checkpoints/cp-{epoch:04d}.ckpt", 
        verbose=1, 
        save_weights_only=True,
        save_freq=8000*BATCH_SIZE)

    # fit the keras model on the dataset
    print("fitting at", timer() - starttime)
    model.fit(xTrain, yTrain, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[cp_callback], verbose=1)

    print("testing at", timer() - starttime)
    testResults = model.evaluate(xTest, yTest, verbose=0)
    print("test results:", testResults)
    return model