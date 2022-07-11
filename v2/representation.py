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
    material = np.zeros(5)

    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()

            if piece == BLANK_PIECE:
                continue

            piece_int = PIECE_TO_INT[piece.lower()]
            if piece.isupper():
                formatted_board[x][y][piece_int] = 1
                if piece.lower() != "k":    # not a king
                    material[piece_int] += 0.1
            else:
                formatted_board[x][y][piece_int] = -1
                if piece.lower() != "k":    # not a king
                    material[piece_int] -= 0.1

    return formatted_board, material