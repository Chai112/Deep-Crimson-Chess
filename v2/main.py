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
# to measure exec time
from timeit import default_timer as timer   

import copy
from operator import itemgetter

BLANK_PIECE = "."

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
#model = train.train(model)
model.load_weights("./checkpoints/test 10/cp-1000.ckpt")

def add_move(possible_moves, from_coord, to_coord):
    #from_coord = coord_to_human(from_coord)
    #to_coord = coord_to_human(to_coord)
    if not from_coord in possible_moves:
        possible_moves[from_coord] = []
    possible_moves[from_coord].append(to_coord)

def is_enemy(piece, is_white_to_move):
    # xor
    a = piece.isupper()
    b = is_white_to_move
    return (a and not b) or (not a and b) # xor

def valid_coord(coord):
    if coord[0] < 0 or coord[0] > 7:
        return False
    if coord[1] < 0 or coord[1] > 7:
        return False
    return True

def enemy_at(board, coord, is_white_to_move):
    if not valid_coord(coord):
        return False

    if empty_at(board, coord):
        return False
    a = is_enemy(board[coord[0]][coord[1]].decode(), is_white_to_move)
    return a

def empty_at(board, coord):
    if not valid_coord(coord):
        return False

    if board[coord[0]][coord[1]].decode() == BLANK_PIECE:
        return True
    return False

def moveable_at(board, coord, is_white_to_move):
    return empty_at(board, coord) or enemy_at(board, coord, is_white_to_move)

def coord_to_human(coord):
    ALPHABET = "abcdefgh"
    y =  8 - coord[0]
    x = coord[1]
    return ALPHABET[x] + str(y)

# --> x
# |
# |
# \/
# y
def find_possible_moves(board, is_white_to_move):
    possible_moves = {}
    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()
            if piece == "P" and is_white_to_move:
                if empty_at(board, (y - 1, x)):
                    add_move(possible_moves, (y, x), (y - 1, x))
                    if y == 6 and empty_at(board, (y - 2, x)):
                        add_move(possible_moves, (y, x), (y - 2, x))

                if enemy_at(board, (y - 1, x - 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y - 1, x - 1))
                if enemy_at(board, (y - 1, x + 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y - 1, x + 1))
            if piece == "p" and not is_white_to_move:
                if empty_at(board, (y + 1, x)):
                    add_move(possible_moves, (y, x), (y + 1, x))
                    if y == 1 and empty_at(board, (y + 2, x)):
                        add_move(possible_moves, (y, x), (y + 2, x))

                if enemy_at(board, (y + 1, x - 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y + 1, x - 1))
                if enemy_at(board, (y + 1, x + 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y + 1, x + 1))
            if piece.lower() == "n" and not is_enemy(piece, is_white_to_move):
                if moveable_at(board, (y - 2, x - 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y - 2, x - 1))
                if moveable_at(board, (y - 1, x - 2), is_white_to_move):
                    add_move(possible_moves, (y, x), (y - 1, x - 2))
                if moveable_at(board, (y - 2, x + 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y - 2, x + 1))
                if moveable_at(board, (y - 1, x + 2), is_white_to_move):
                    add_move(possible_moves, (y, x), (y - 1, x + 2))
                if moveable_at(board, (y + 2, x - 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y + 2, x - 1))
                if moveable_at(board, (y + 1, x - 2), is_white_to_move):
                    add_move(possible_moves, (y, x), (y + 1, x - 2))
                if moveable_at(board, (y + 2, x + 1), is_white_to_move):
                    add_move(possible_moves, (y, x), (y + 2, x + 1))
                if moveable_at(board, (y + 1, x + 2), is_white_to_move):
                    add_move(possible_moves, (y, x), (y + 1, x + 2))
            if piece.lower() == "b" and not is_enemy(piece, is_white_to_move):
                i = 0
                while True:
                    i = i + 1
                    coord = (y - i, x - i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y - i, x + i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y + i, x - i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y + i, x + i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
            if piece.lower() == "r" and not is_enemy(piece, is_white_to_move):
                i = 0
                while True:
                    i = i + 1
                    coord = (y - i, x)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y + i, x)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y, x - i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y, x + i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
            if piece.lower() == "q" and not is_enemy(piece, is_white_to_move):
                i = 0
                while True:
                    i = i + 1
                    coord = (y - i, x - i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y - i, x + i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y + i, x - i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y + i, x + i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y - i, x)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y + i, x)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y, x - i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break
                i = 0
                while True:
                    i = i + 1
                    coord = (y, x + i)
                    if moveable_at(board, coord, is_white_to_move):
                        add_move(possible_moves, (y, x), coord)
                    else:
                        break
                    if enemy_at(board, coord, is_white_to_move):
                        break


            if piece.lower() == "k" and not is_enemy(piece, is_white_to_move):
                for i in range(3):
                    for j in range(3):
                        if not (i == 1 and j == 1):
                            if moveable_at(board, (y - 1 + j, x - 1 + i), is_white_to_move):
                                add_move(possible_moves, (y, x), (y - 1 + j, x - 1 + i))

    possible_moves_final = []
    for move_from in possible_moves:
        for move_to in possible_moves[move_from]:
            possible_moves_final.append({"from": move_from, "to": move_to})
    return possible_moves_final

def generate_scenarios_from_moves(board, possible_moves):
    for move in possible_moves:
        new_board = copy.copy(board) # copy list
        move_from = move["from"]
        move_to = move["to"]
        piece = new_board[move_from[0]][move_from[1]].decode()
        new_board[move_from[0]][move_from[1]] = BLANK_PIECE
        new_board[move_to[0]][move_to[1]] = piece
        move["board"] = new_board
        #print(coord_to_human(move_from), "->", coord_to_human(move_to))
                


while True:
    print("input FEN")
    userFen = input()
    board, extraInfo = representation.evaluateFenIntoBoard(userFen)
    displayBoard(board, extraInfo)
    flatBoard = representation.flattenBoard(board, extraInfo)
    prediction = model.predict([flatBoard])
    print(prediction)
    print("this is equivalent to being", (prediction[0][0]) * 20, "pawns up")

    is_white_to_move = extraInfo["whoseMove"] == "w"
    possible_moves = find_possible_moves(board, is_white_to_move)
    generate_scenarios_from_moves(board, possible_moves)

    starttime = timer()
    print("evaluating =====================================")
    for scenario in possible_moves:
        flatBoard = representation.flattenBoard(scenario["board"], extraInfo)
        prediction = model.predict([flatBoard])
        scenario["prediction"] = prediction[0]

    possible_moves_sorted = sorted(possible_moves, key=itemgetter('prediction'), reverse=is_white_to_move) 
    best_move = possible_moves_sorted[0]
    move_from = best_move["from"]
    move_to = best_move["to"]
    print("depth 1 at", timer() - starttime, "s")
    print("BEST MOVE:", coord_to_human(move_from), "->", coord_to_human(move_to))


#print("input FEN")
#userFen = input()
#board, extraInfo = representation.evaluateFenIntoBoard(userFen)
#displayBoard(board, extraInfo)
#flatBoard = representation.flattenBoard(board, extraInfo)
#print(flatBoard)
