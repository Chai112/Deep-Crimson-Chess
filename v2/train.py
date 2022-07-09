import numpy as np
import csv
import tensorflow as tf
import tensorflow.keras
from tensorflow.keras import layers, models, callbacks
import representation

# to measure exec time
from timeit import default_timer as timer   
import matplotlib.pyplot as plt

TESTING_SIZE = 100
EPOCHS = 200
DATASET = "../datasets/chessData-small.csv"
MAX_EVAL = 2000 # in centipawns

def create_model():
    inputA = tf.keras.Input(shape=(8, 8, 6))
    inputB = tf.keras.Input(shape=(5,))

    x = layers.Conv2D(16, 3, activation='tanh', padding='same')(inputA)
    x = layers.MaxPooling2D((2, 2), padding='same')(x)
    x = layers.Conv2D(32, 3, activation='tanh', padding='same')(x)
    x = layers.MaxPooling2D((2, 2), padding='same')(x)
    x = layers.Conv2D(32, 3, activation='tanh', padding='same')(x)
    x = layers.Flatten()(x)
    x = tf.keras.Model(inputs=inputA, outputs=x)

    #y = layers.Dense(5, activation="tanh")(inputB)
    #y = tf.keras.Model(inputs=inputB, outputs=y)

    # combine the output of the two branches
    combined = layers.concatenate([x.output, inputB])

    fc = layers.Dense(16, activation='tanh')(combined)
    fc = layers.Dense(4, activation='tanh')(fc)
    fc = layers.Dense(1)(fc)
    model = tf.keras.Model(inputs= [x.input, inputB], outputs = fc)
    model.summary()

    model.compile(optimizer='adam',
                loss='mse',
                metrics=['accuracy'])
    return model

def train(model):
    print("start")
    starttime = timer()

    with open(DATASET, newline='') as csvfile:
        dataset = list(csv.reader(csvfile))
    dataset = dataset[1:] # remove column names
    print("data loaded at", timer() - starttime)

    train_boards = np.zeros((len(dataset), 8,8,6))
    train_attr = np.zeros((len(dataset), 5))
    train_evals = np.zeros(len(dataset))

    N = 0
    for n in range(len(dataset)):
        fen = dataset[n][0]
        evaluation = dataset[n][1]

        board, extraInfo = representation.evaluateFenIntoBoard(fen)
        if evaluation[0] == "#":  # if evaluation is mate in...
            if evaluation[1] == "+": # if mate in ... is to black
                evaluation = str(MAX_EVAL)
            else:
                evaluation = str(-MAX_EVAL)
        if extraInfo == {}: # invalid FEN
            continue

        formatted_board, attr = representation.format_board(board)
        train_boards[N] = formatted_board
        train_attr[N] = attr
        # clamp evaluations to +/-1000 and normalise to 0-1
        formatted_evaluation = max(0, min(1, float(evaluation) / MAX_EVAL))
        train_evals[N] = formatted_evaluation
        N = N + 1

    del dataset

    # trim white to moves
    train_boards = train_boards[:N]
    train_evals = train_evals[:N]
    train_attr = train_attr[:N]

    xTrainBoards = train_boards[:-TESTING_SIZE]
    xTrainAttrs = train_attr[:-TESTING_SIZE]
    yTrain = train_evals[:-TESTING_SIZE]

    xTestBoards = train_boards[-TESTING_SIZE:]
    xTestAttrs = train_attr[-TESTING_SIZE:]
    yTest = train_evals[-TESTING_SIZE:]

    print("FENs cleaned & flattened at", timer() - starttime)
    print("data size:", len(train_boards))

    del train_boards
    del train_evals

    # Create a callback that saves the model's weights every 5 epochs
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath="./checkpoints/cp-{epoch:04d}.ckpt", 
        verbose=1, 
        save_weights_only=True,
        save_freq=8000*32)

    # fit the keras model on the dataset
    print("fitting at", timer() - starttime)

    history = model.fit(x = [xTrainBoards, xTrainAttrs],y= yTrain, epochs=EPOCHS, callbacks=[cp_callback], verbose=1, validation_data=([xTestBoards, xTestAttrs], yTest))

    print(history)
    plt.plot(history.history['loss'], label='loss')
    #plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.show()

    test_loss, test_acc = model.evaluate([xTestBoards, xTestAttrs], yTest, verbose=2)
    print("test accuracy:", test_acc)

    return model