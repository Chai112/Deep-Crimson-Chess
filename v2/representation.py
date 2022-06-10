import numpy as np

BLANK_PIECE = "."
PIECES = "PNBRQKpnbrqk"

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

    board =np.empty([8,8], dtype='S')
    board.fill(BLANK_PIECE)

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
        return [], {} # we don't do that here!

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

def flattenBoard (board, extraInfo):
    flatBoards = {}

    for piece in PIECES:
        flatBoards[piece]=np.empty([8,8], dtype='f')
        flatBoards[piece].fill(0.0)

    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()
            if piece != BLANK_PIECE:
                flatBoards[piece][y][x] = 1.0

    flatBoard = []
    #flatBoard.append(1.0 if extraInfo["canWhiteCastleKingside"] else 0.0)
    #flatBoard.append(1.0 if extraInfo["canWhiteCastleQueenside"] else 0.0)
    #flatBoard.append(1.0 if extraInfo["canBlackCastleKingside"] else 0.0)
    #flatBoard.append(1.0 if extraInfo["canBlackCastleQueenside"] else 0.0)
    #flatBoard.append(float(extraInfo["halfmoveClock"]))

    for piece in PIECES:
        for y in range(8):
            for x in range(8):
                flatBoard.append(float(flatBoards[piece][y][x]))
    return flatBoard