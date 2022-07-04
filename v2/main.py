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
from tensorflow import keras
import representation
import train
import chess
# to measure exec time
from timeit import default_timer as timer   
from operator import itemgetter

import matplotlib.pyplot as plt

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

model = train.create_model()
model = train.train(model)
#model.load_weights("./checkpoints/test 10/cp-1000.ckpt")

while True:
    print("input FEN")
    userFen = input()
    board, extraInfo = representation.evaluateFenIntoBoard(userFen)
    displayBoard(board, extraInfo)

    formatted_board = representation.format_board(board)
    prediction = model.predict(np.array([formatted_board]))
    print(prediction)
    print("this is equivalent to being", (prediction[0][0]) * 20, "pawns up")

    is_white_to_move = extraInfo["whoseMove"] == "w"
    possible_moves = chess.find_possible_moves(board, is_white_to_move)
    chess.generate_scenarios_from_moves(board, possible_moves)

    starttime = timer()
    print("evaluating =====================================")
    for scenario in possible_moves:
        formatted_board = representation.format_board(scenario["board"])
        prediction = model.predict(np.array([formatted_board]))
        scenario["prediction"] = prediction[0]

    possible_moves_sorted = sorted(possible_moves, key=itemgetter('prediction'), reverse=is_white_to_move) 
    best_move = possible_moves_sorted[0]
    move_from = best_move["from"]
    move_to = best_move["to"]
    print("depth 1 at", timer() - starttime, "s")
    print("BEST MOVE:", chess.coord_to_human(move_from), "->", chess.coord_to_human(move_to))


#print("input FEN")
#userFen = input()
#board, extraInfo = representation.evaluateFenIntoBoard(userFen)
#displayBoard(board, extraInfo)
#flatBoard = representation.flattenBoard(board, extraInfo)
#print(flatBoard)
