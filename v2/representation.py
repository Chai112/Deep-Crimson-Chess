import numpy as np

BLANK_PIECE = "."
PIECES = "Ppnbrqk"
MATERIAL_PIECES = "pnbrq"

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
    if whoseMove == "w": # we dont do that here
        return [], {}

    enpassantSquare = fen[3]

    extraInfo = {
        "canWhiteCastleKingside": canWhiteCastleKingside,
        "canWhiteCastleQueenside": canWhiteCastleQueenside,
        "canBlackCastleKingside": canBlackCastleKingside,
        "canBlackCastleQueenside": canBlackCastleQueenside,
        "enpassantSquare": enpassantSquare,
        "halfmoveClock": halfmoveClock,
        "whoseMove": whoseMove,
    }
    return board, extraInfo

PIECE_TO_INT = {
    "p": 0,
    "n": 1,
    "b": 2,
    "r": 3,
    "q": 4,
    "k": 5,
}
def format_board (board):
    formatted_board = np.zeros((8, 8, 6))
    formatted_board.fill(0.5)

    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()

            if piece == BLANK_PIECE:
                continue

            piece_int = PIECE_TO_INT[piece.lower()]
            if piece.isupper():
                formatted_board[x][y][piece_int] = 1
            else:
                formatted_board[x][y][piece_int] = -1

    return formatted_board
    

def flattenBoard (board, extraInfo):
    flatBoards = {}

    for piece in PIECES:
        flatBoards[piece]=np.empty([8,8], dtype='f')
        flatBoards[piece].fill(0.0)

    material = {}
    for piece in MATERIAL_PIECES:
        material[piece] = 0.0

    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()
            if piece != BLANK_PIECE:
                if piece.lower() == "p":
                    flatBoards[piece][y][x] = 1.0
                else:
                    if piece.isupper():
                        flatBoards[piece.lower()][y][x] = 1.0
                    else:
                        flatBoards[piece][y][x] = -1.0

                # count material
                if piece.lower() in MATERIAL_PIECES:
                    if piece.isupper():
                        material[piece.lower()] = material[piece.lower()] + 0.1
                    else:
                        material[piece.lower()] = material[piece.lower()] - 0.1

    flatBoard = []
    #flatBoard.append(1.0 if extraInfo["canWhiteCastleKingside"] else 0.0)
    #flatBoard.append(1.0 if extraInfo["canWhiteCastleQueenside"] else 0.0)
    #flatBoard.append(1.0 if extraInfo["canBlackCastleKingside"] else 0.0)
    #flatBoard.append(1.0 if extraInfo["canBlackCastleQueenside"] else 0.0)
    #flatBoard.append(float(extraInfo["halfmoveClock"]))
    for piece in MATERIAL_PIECES:
        flatBoard.append(material[piece])

    for piece in PIECES:
        for y in range(8):
            for x in range(8):
                flatBoard.append(float(flatBoards[piece][y][x]))
    #print(len(flatBoard));
    return flatBoard