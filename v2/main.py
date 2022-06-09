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

# extra info
def evaluateFenIntoBoard(userFen):
    fen = userFen.split()

    canWhiteCastleKingside = False
    canWhiteCastleQueenside = False
    canBlackCastleKingside = False
    canBlackCastleQueenside = False
    halfmoveClock = 0

    enpassantSquare = "-"

    x = 0;
    y = 0;
    fenPosition = fen[0]
    for idx, char in enumerate(fenPosition):
        if char.isnumeric():
            x = x + int(char)
        elif char == "/":
            y = y + 1
            x = 0
        else:
            board[y][x] = char
            x = x + 1

    canWhiteCastleKingside = "K" in fen[2]
    canWhiteCastleQueenside = "Q" in fen[2]
    canBlackCastleKingside = "k" in fen[2]
    canBlackCastleQueenside = "q" in fen[2]
    halfmoveClock = fen[4]

    whoseMove = fen[1]
    if (whoseMove == "w"):
        return # we don't do that here!

    enpassantSquare = fen[3]

    extraInfo = {
        "canWhiteCastleKingside": canWhiteCastleKingside,
        "canWhiteCastleQueenside": canWhiteCastleQueenside,
        "canBlackCastleKingside": canBlackCastleKingside,
        "canBlackCastleQueenside": canBlackCastleQueenside,
        "enpassantSquare": enpassantSquare,
        "halfmoveClock": halfmoveClock
    }
    return board, extraInfo

def createMetaBoard (board, extraInfo):
    metaBoards = {}

    for piece in PIECES:
        metaBoards[piece]=np.empty([8,8], dtype='f')
        metaBoards[piece].fill(0.0)

    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()
            if piece != BLANK_PIECE:
                metaBoards[piece][y][x] = 1.0

    metaBoard = []
    metaBoard.append(1 if extraInfo["canWhiteCastleKingside"] else 0)
    metaBoard.append(1 if extraInfo["canWhiteCastleQueenside"] else 0)
    metaBoard.append(1 if extraInfo["canBlackCastleKingside"] else 0)
    metaBoard.append(1 if extraInfo["canBlackCastleQueenside"] else 0)
    metaBoard.append(1 if extraInfo["halfmoveClock"] else 0)

    for piece in PIECES:
        for y in range(8):
            for x in range(8):
                metaBoard.append(metaBoards[piece][y][x])
    return metaBoard

print("start")

BLANK_PIECE = "."
PIECES = "PNBRQKpnbrqk"
board =np.empty([8,8], dtype='S')
board.fill(BLANK_PIECE)

print("input FEN")
userFen = input()
print("a")
board, extraInfo = evaluateFenIntoBoard(userFen)
displayBoard(board, extraInfo)
metaBoard = createMetaBoard(board, extraInfo)
print(metaBoard)
