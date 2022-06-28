# SHCR - Shallow Crimson
# Developed by Chaidhat Chaimongkol on 9 June, 2022

# install anaconda
# go here https://docs.anaconda.com/anaconda/user-guide/tasks/tensorflow/
# this is helpful https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/
# also this https://machinelearningmastery.com/setup-python-environment-machine-learning-deep-learning-anaconda/
# conda activate tf
# pip install --upgrade numpy, keras, matplotlib, seaborn # dont forget to conda deactivate (but its ok if you dont) #
# to run:
# conda activate tf
# python3 tf-test.py

# there are 12 types of ieces: PNBRQKpnbrqk (capital letters for white)
# there are 64 squares
# there are 5 extra info (see below)
# so there needs to be 12*64 + 5 = 773 inputs input for the NN

# limitations:
# the engine does not consider en passants in its evaluations
# the engine can only play as black


import numpy as np
import csv
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow import keras
import tensorflow.keras.callbacks as carl
import time

import representation
# to measure exec time
from timeit import default_timer as timer   
  
def displayBoard(board, extraInfo):
    for y in range(8):
        print(8-y, "| ", end="")
        for x in range(8):
            print(board[y][x].decode() + " ", end="")
        print("")
    print("   ----------------")
    print("    a b c d e f g h")
    print("can white castle kingside? ",  extraInfo["canWhiteCastleKingside"])
    print("can white castle queenside? ", extraInfo["canWhiteCastleQueenside"])
    print("can black castle kingside? ",  extraInfo["canBlackCastleKingside"])
    print("can black castle queenside? ", extraInfo["canBlackCastleQueenside"])
    print("enpassant square: ", extraInfo["enpassantSquare"])
    print("halfmove clock: ", extraInfo["halfmoveClock"])

print("start")
starttime = timer()
# Create a new model instance
model = Sequential()
model.add(Dense(64, input_dim=768, activation='tanh'))
model.add(Dense(64, activation='tanh'))
model.add(Dense(16, activation='tanh'))
model.add(Dense(16, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(1, activation='tanh'))
# compile the keras model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

TESTING_SIZE = 1000

with open('../datasets/chessData-small.csv', newline='') as csvfile:
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
            groundEvaluation = "10000"
        else:
            groundEvaluation = "-10000"
    if extraInfo == {}: # invalid FEN
        continue
    #print("evaluation: ", groundEvaluation)
    #displayBoard(board, extraInfo)
    flatBoard = representation.flattenBoard(board, extraInfo)
    flatBoards.append(flatBoard)
    groundEvaluation2 = max(-1, min(1, float(groundEvaluation) / 10000))
    groundEvaluations.append(groundEvaluation2) # clamp groundEvaluation to +/-10000 and normalise to 0-1

del dataset

xTrain = flatBoards[:-TESTING_SIZE]
yTrain = groundEvaluations[:-TESTING_SIZE]

xTest = flatBoards[-TESTING_SIZE:]
yTest = groundEvaluations[-TESTING_SIZE:]

print("FENs cleaned & flattened at", timer() - starttime)
print("number of valid flatboards", len(flatBoards))

del flatBoards
del groundEvaluations

model = Sequential()
model.add(Dense(64, input_dim=768, activation='tanh'))
model.add(Dense(64, activation='tanh'))
model.add(Dense(16, activation='tanh'))
model.add(Dense(16, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(8, activation='tanh'))
model.add(Dense(1, activation='tanh'))
# compile the keras model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

BATCH_SIZE = 100
# Create a callback that saves the model's weights every 5 epochs
cp_callback = keras.callbacks.ModelCheckpoint(
    filepath="./checkpoints/cp-{epoch:04d}.ckpt", 
    verbose=1, 
    save_weights_only=True,
    save_freq=500*BATCH_SIZE)

# fit the keras model on the dataset
print("fitting at", timer() - starttime)
model.fit(xTrain, yTrain, epochs=1000, batch_size=BATCH_SIZE, callbacks=[cp_callback], verbose=1)

print("testing at", timer() - starttime)
testResults = model.evaluate(xTest, yTest, verbose=0)
print("test results:", testResults)
# Save the weights
model.save_weights('./checkpoints/my_checkpoint_FINAL.ckpt')

correct = 0
tested = 0
for n in range(TESTING_SIZE):
    prediction = model.predict([xTest[n]])[0][0]
    if yTest[n] == 0.5:
        continue

    tested = tested + 1
    if (yTest[n] > 0 and prediction > 0) or (yTest[n] <0 and prediction < 0):
        #print("prediction", prediction, "ground", yTest[n], "right", correct)
        correct = correct + 1
    #else:
        #print("prediction", prediction, "ground", yTest[n], "wrong")
print("correct side:", correct, "of", tested, "times (", (correct / tested) * 100, "%)")

while True:
    print("input FEN")
    userFen = input()
    board, extraInfo = representation.evaluateFenIntoBoard(userFen)
    if extraInfo == {}:
        print("make sure it is black to move")
        continue
    displayBoard(board, extraInfo)
    flatBoard = representation.flattenBoard(board, extraInfo)
    prediction = model.predict([flatBoard])
    print(prediction)
    print("this is equivalent to being", (prediction[0][0]) * 100, "pawns up")

#print("input FEN")
#userFen = input()
#board, extraInfo = representation.evaluateFenIntoBoard(userFen)
#displayBoard(board, extraInfo)
#flatBoard = representation.flattenBoard(board, extraInfo)
#print(flatBoard)
