# Deep Crimson
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
import train
import play
import chess
import representation

import matplotlib.pyplot as plt

MAX_EVAL = 2000 # in centipawns
START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def displayBoard(board, extraInfo):
    for y in range(8):
        print(8-y, "| ", end="")
        for x in range(8):
            print(board[y][x].decode() + " ", end="")
        print("")
    print("   ----------------")
    print("    a b c d e f g h")
    #print("can white castle kingside? ",  extraInfo["canWhiteCastleKingside"])
    #print("can white castle queenside? ", extraInfo["canWhiteCastleQueenside"])
    #print("can black castle kingside? ",  extraInfo["canBlackCastleKingside"])
    #print("can black castle queenside? ", extraInfo["canBlackCastleQueenside"])
    #print("enpassant square: ", extraInfo["enpassantSquare"])
    #jjjprint("halfmove clock: ", extraInfo["halfmoveClock"])

def format_eval(eval):
    prefix = ""
    if eval > 0:
        prefix = "+"
    return prefix + f'{eval * MAX_EVAL * 0.01:.3}'


model = train.create_model()
#model = train.train(model)
model.load_weights("./checkpoints/test 15/cp-0130.ckpt")

while True:
    print("input FEN")
    userFen = input()

    # if input is empty, default to default board
    if userFen == "":
        userFen = START

    # convert FEN to board
    board, extraInfo = representation.evaluateFenIntoBoard(userFen)
    displayBoard(board, extraInfo)

    # format board for NN
    formatted_board, attr = representation.format_board(board)
    is_white_to_move = extraInfo["whoseMove"] == "w"

    # predict
    eval_init = model.predict([np.array([formatted_board]), np.array([attr])])[0][0]
    print("")
    print("init eval:\t", format_eval(eval_init), "pawns")
    print("")

    i = 0
    while i < 50:
        print(str(i + 1) + ". ", end = "")
        j = 0
        while j < 2:
            # find best move
            best_scenario = play.find_best_move(model, board, is_white_to_move, 1)
            if len(best_scenario) == 0:
                if not is_white_to_move:
                    print("1-0")
                    i = 1000000
                    break
                else:
                    i = 1000000
                    print("0-1")
                    break
            best_move_seq = best_scenario["move_sequence"]
            best_move_seq.reverse()
            move = [{"move": best_move_seq[0]}]
            board = chess.generate_boards_from_moves(board, move)[0]["board"]
            moveStr = str(str(chess.coord_to_human(best_move_seq[0]["from"])) + str(chess.coord_to_human(best_move_seq[0]["to"])))
            is_white_to_move = not is_white_to_move
            print(moveStr + " ", end = "")
            j += 1
        
        print("")
        i += 1
        #print(displayBoard(board,{}))

    #print("")
    #print("BEST MOVE:")
    #for best_move in best_move_seq:
    #    if (best_move == "white checkmated" 
    #    or best_move == "black checkmated" 
    #    or best_move == "stalemate"):
    #        print(best_move)
    #    else:
    #        move_from = best_move["from"]
    #        move_to = best_move["to"]
    #        print(chess.coord_to_human(move_from), "->", chess.coord_to_human(move_to))

    print("\n\n")