import copy

BLANK_PIECE = '.'

def add_move(possible_moves, from_coord, to_coord):
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

def is_king_in_check(board, is_white_to_move):
    opponents_possible_moves = find_possible_moves(board, not is_white_to_move, False)
    king_x = -1 
    king_y = -1 
    # locate king
    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()
            if (is_white_to_move and piece == "K") or (not is_white_to_move and piece == "k"):
                king_x = x
                king_y = y
                break
    # check if opponent is checking the king
    if not (king_x == -1 or king_y == -1):
        for move in opponents_possible_moves:
            if move["move"]["to"] == (king_y, king_x):
                return True, opponents_possible_moves
        return False, opponents_possible_moves
    else:
        print(board)
        print("No king is present on the board")
        exit()

# --> x
# |
# |
# \/
# y
def find_possible_moves(board, is_white_to_move, check_for_checks = True):

    if check_for_checks:
        king_in_check, opponents_possible_moves = is_king_in_check(board, is_white_to_move)
    else:
        king_in_check = False

    possible_moves = {}
    for y in range(8):
        for x in range(8):
            piece = board[y][x].decode()
            if piece == "P" and is_white_to_move:
                if (empty_at(board, (y - 1, x))
                    and check_for_checks): # for opposite calculation, pawn isn't attacking ahead
                    add_move(possible_moves, (y, x), (y - 1, x))
                    if y == 6 and empty_at(board, (y - 2, x)):
                        add_move(possible_moves, (y, x), (y - 2, x))

                if (enemy_at(board, (y - 1, x - 1), is_white_to_move)
                    or not check_for_checks): # for opposite calculation, pawn attacking king
                    add_move(possible_moves, (y, x), (y - 1, x - 1))
                if (enemy_at(board, (y - 1, x + 1), is_white_to_move)
                    or not check_for_checks): # for opposite calculation, pawn attacking king
                    add_move(possible_moves, (y, x), (y - 1, x + 1))
            if piece == "p" and not is_white_to_move:
                if (empty_at(board, (y + 1, x))
                    and check_for_checks): # for opposite calculation, pawn isn't attacking ahead
                    add_move(possible_moves, (y, x), (y + 1, x))
                    if y == 1 and empty_at(board, (y + 2, x)):
                        add_move(possible_moves, (y, x), (y + 2, x))

                if (enemy_at(board, (y + 1, x - 1), is_white_to_move)
                    or not check_for_checks): # for opposite calculation, pawn attacking king
                    add_move(possible_moves, (y, x), (y + 1, x - 1))
                if (enemy_at(board, (y + 1, x + 1), is_white_to_move)
                    or not check_for_checks): # for opposite calculation, pawn attacking king
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

                # check castling position
                if (is_white_to_move and x == 4 and y == 7) or (not is_white_to_move and x == 4 and y == 0):

                    # if not checking for checks, then it will recursively loop forever
                    if check_for_checks and not king_in_check:
                        # kingside
                        # check if the space is clear
                        if (empty_at(board, (y, x + 1)) 
                        and empty_at(board, (y, x + 2))):
                            # check if rook is there
                            if ((is_white_to_move and board[y][x + 3].decode() == "R") 
                            or (not is_white_to_move and board[y][x + 3].decode() == "r")):
                                can_castle = True
                                for move in opponents_possible_moves:
                                    if (move["move"]["to"] == (y, x + 1) 
                                    or move["move"]["to"] == (y, x + 2)):
                                        can_castle = False
                                if can_castle:
                                    add_move(possible_moves, (y, x), (y, x + 2))

                        # queenside
                        # check if the space is clear
                        if (empty_at(board, (y, x - 1)) 
                        and empty_at(board, (y, x - 2))
                        and empty_at(board, (y, x - 3))):
                            # check if rook is there
                            if ((is_white_to_move and board[y][x - 4].decode() == "R") 
                            or (not is_white_to_move and board[y][x - 4].decode() == "r")):
                                can_castle = True
                                for move in opponents_possible_moves:
                                    if (move["move"]["to"] == (y, x - 1) 
                                    or move["move"]["to"] == (y, x - 2)
                                    or move["move"]["to"] == (y, x - 3)):
                                        can_castle = False
                                if can_castle:
                                    add_move(possible_moves, (y, x), (y, x - 2))


    possible_moves_final = []
    for move_from in possible_moves:
        for move_to in possible_moves[move_from]:
            possible_moves_final.append({"move": {"from": move_from, "to": move_to}})
        
    # check if moves are legal => only a concern if King is in check
    #print("is king in check?", king_in_check)
    if check_for_checks:
        scenarios = generate_boards_from_moves(board, possible_moves_final)
        possible_moves_final = []
        for scenario in scenarios:
            king_still_in_check, _ = is_king_in_check(scenario["board"], is_white_to_move)
            if not king_still_in_check:
                #print(coord_to_human(scenario["move"]["from"]), "->", coord_to_human(scenario["move"]["to"]))
                possible_moves_final.append({"move": {"from": scenario["move"]["from"], "to": scenario["move"]["to"]}})
    
    # check for checkmate
    if len(possible_moves_final) == 0:
        if king_in_check:
            return "checkmate"
        else:
            return "stalemate"

    return possible_moves_final

def generate_boards_from_moves(board, possible_moves):
    scenarios = []
    for move in possible_moves:
        new_board = copy.copy(board) # copy list

        move_from = move["move"]["from"]
        move_to = move["move"]["to"]
        piece = new_board[move_from[0]][move_from[1]].decode()

        new_board[move_from[0]][move_from[1]] = BLANK_PIECE
        new_board[move_to[0]][move_to[1]] = piece

        # is castling kingside?
        if piece.lower() == "k":
            if move_to[1] - move_from[1] == 2:
                rook_piece = new_board[move_from[0]][7].decode()
                new_board[move_from[0]][7] = BLANK_PIECE
                new_board[move_to[0]][5] = rook_piece
            # is castling queenside?
            if move_to[1] - move_from[1] == -2:
                rook_piece = new_board[move_from[0]][0].decode()
                new_board[move_from[0]][0] = BLANK_PIECE
                new_board[move_to[0]][3] = rook_piece

        scenario = {}
        scenario["move"] = move["move"]
        scenario["board"] = new_board
        scenarios.append(scenario)
        #print(coord_to_human(move_from), "->", coord_to_human(move_to))
    return scenarios