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
from progress.bar import Bar

MAX_EVAL = 2000 # in centipawns

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

count = 0
def countt():
    global count
    count = count + 1
    if count % 100 == 0:
        print(count)

def min_max(board, is_white_to_move, depth):

    possible_moves = chess.find_possible_moves(board, is_white_to_move)
    scenarios = chess.generate_boards_from_moves(board, possible_moves)

    final_scenarios = []

    # profiling
    if depth == 1:
        bar = Bar('depth ' + str(depth), max=len(scenarios))

    if depth == 0:
        formatted_boards = []
        attrs = []
        for scenario in scenarios:
            #countt()
            formatted_board, attr = representation.format_board(scenario["board"])
            formatted_boards.append(formatted_board)
            attrs.append(attr)

        prediction = model.predict([np.array(formatted_boards), np.array(attrs)])

        for idx, scenario in enumerate(scenarios):
            scenario["prediction"] = prediction[idx]
            final_scenarios.append(scenario)
    else:
        for scenario in scenarios:
            # profiling
            if depth == 1:
                bar.next()
            # recursively min-max
            final_scenario = min_max(scenario["board"], not is_white_to_move, depth - 1)
            final_scenario["move_sequence"].append(scenario["move_sequence"][0])
            final_scenarios.append(final_scenario)


    # profiling
    if depth == 1:
        bar.finish()

    # sort from most favourable to least favourable
    final_scenarios_sorted = sorted(final_scenarios, key=itemgetter('prediction'), reverse= is_white_to_move) 
    final_scenario = final_scenarios_sorted[0]
    return final_scenario

model = train.create_model()
#model = train.train(model)
model.load_weights("./checkpoints/test 14/cp-0200.ckpt")

while True:
    print("input FEN")
    userFen = input()

    # convert FEN to board
    board, extraInfo = representation.evaluateFenIntoBoard(userFen)
    displayBoard(board, extraInfo)

    # format board for NN
    formatted_board, attr = representation.format_board(board)
    print(attr)
    is_white_to_move = extraInfo["whoseMove"] == "w"

    if is_white_to_move:
        print("black to move only")
        continue

    # predict
    eval_init = model.predict([np.array([formatted_board]), np.array([attr])])[0][0]
    print("")
    print("init eval:\t", format_eval(eval_init), "pawns")
    print("")

    # find next best move
    starttime = timer()
    best_scenario = min_max(board, is_white_to_move, 1)
    eval_time = timer()
    print("eval time:\t", f'{eval_time - starttime:.3}', "s")

    best_move_seq = best_scenario["move_sequence"]
    best_move_seq.reverse()
    eval_post = float(best_scenario["prediction"])
    print("post eval:\t", format_eval(eval_post), "pawns")
    print("delta eval:\t", format_eval(eval_post - eval_init), "pawns")

    print("")
    for best_move in best_move_seq:
        move_from = best_move["from"]
        move_to = best_move["to"]
        print("BEST MOVE:", chess.coord_to_human(move_from), "->", chess.coord_to_human(move_to))

    print("\n\n")



#print("input FEN")
#userFen = input()
#board, extraInfo = representation.evaluateFenIntoBoard(userFen)
#displayBoard(board, extraInfo)
#flatBoard = representation.flattenBoard(board, extraInfo)
#print(flatBoard)
