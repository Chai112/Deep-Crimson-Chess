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

print("input FEN")
userFen = input()
board, extraInfo = representation.evaluateFenIntoBoard(userFen)
displayBoard(board, extraInfo)
flatBoard = representation.flattenBoard(board, extraInfo)
print(flatBoard)
