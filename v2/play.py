from timeit import default_timer as timer   
from operator import itemgetter
import numpy as np

import chess
import representation

def find_all_moves(board, is_white_to_move, depth):

    global moves_board
    global moves_attr

    possible_moves = chess.find_possible_moves(board, is_white_to_move)
    if possible_moves == "checkmate" or possible_moves == "stalemate":
        scenario = {}
        scenario["children"] = []
        if possible_moves == "checkmate":
            if is_white_to_move:
                scenario["special"] = "white checkmated"
            else:
                scenario["special"] = "black checkmated"
        else:
            scenario["special"] = "stalemate"
        return [scenario]
    else:
        scenarios = chess.generate_boards_from_moves(board, possible_moves)

    for scenario in scenarios:
        # format the board and set to hash table
        if depth == 0:
            formatted_board, attr = representation.format_board(scenario["board"])
            formatted_board.flags.writeable = False

            board_hash_idx = len(moves_board)

            moves_board.append(formatted_board)
            moves_attr.append(attr)

            scenario["board_hash_idx"] = board_hash_idx

        else:
            # recursively find all moves
            final_scenarios = find_all_moves(scenario["board"], not is_white_to_move, depth - 1)
            scenario["children"] = []
            for final_scenario in final_scenarios:
                scenario["children"].append(final_scenario)

    # return
    return scenarios

def min_max(scenarios, is_white_to_move, depth):
    global moves_eval

    final_scenarios = []

    for scenario in scenarios:
        if "special" in scenario.keys():
            scenario["move"] = scenario["special"]
            if scenario["special"] == "white checkmated":
                scenario["prediction"] = -100000
            elif scenario["special"] == "black checkmated":
                scenario["prediction"] = 100000
            elif scenario["special"] == "stalemate":
                scenario["prediction"] = 0

        if depth == 0:
            if not "special" in scenario.keys():
                scenario["prediction"] = moves_eval[scenario["board_hash_idx"]]

            scenario["move_sequence"] = [scenario["move"]]
            final_scenarios.append(scenario)
        else:
            # recursively min-max
            if not len(scenario["children"]) == 0:
                final_scenario = min_max(scenario["children"], not is_white_to_move, depth - 1)
            else: # no children exist
                final_scenario = scenario

            if not "move_sequence" in final_scenario.keys():
                scenario["move_sequence"] = []

            final_scenario["move_sequence"].append(scenario["move"])
            final_scenarios.append(final_scenario)

    final_scenarios_sorted = sorted(final_scenarios, key=itemgetter('prediction'), reverse= is_white_to_move) 
    final_scenario = final_scenarios_sorted[0]
    return final_scenario

# [formatted_board]: {attr: 0, prediction: 0}

# scenario 1:
#   move: [e4, e5]
#   board: [[...]]
#   children:
#     scenario 2:
#        ...

def find_best_move(model, board, is_white_to_move, max_depth, verbose = False):
    global moves_board
    global moves_attr
    global moves_eval

    moves_board = []
    moves_attr = []
    moves_eval = []
    # find next best move
    if verbose:
        print("finding best move...")
    starttime = timer()
    final_scenarios = find_all_moves(board, is_white_to_move, max_depth)
    search_time = timer()

    if len(moves_board) == 0:
        return []

    moves_eval = model.predict([np.array(moves_board), np.array(moves_attr)])
    eval_time = timer()

    if verbose:
        print("search time:\t", f'{search_time-starttime:.3}', "s")
        print("moves found:\t", len(moves_board), "positions")
        print("eval time:\t", f'{eval_time - search_time:.3}', "s")

    best_scenario = min_max(final_scenarios, is_white_to_move, max_depth)

    minmax_time = timer()
    if verbose:
        print("minmax time:\t", f'{minmax_time - eval_time:.3}', "s")
        print("total time:\t", f'{eval_time - starttime:.3}', "s")
        print("eval rate:\t", len(moves_board) / (eval_time - starttime), "moves/s")
        eval_post = float(best_scenario["prediction"])
        print("post eval:\t", format_eval(eval_post), "pawns")
        print("delta eval:\t", format_eval(eval_post - eval_init), "pawns")
    return best_scenario

def do_best_move(board, best_scenario):
    best_move_seq = best_scenario["move_sequence"]
    best_move_seq.reverse()
    move = [{"move": best_move_seq[0]}]
    new_board = chess.generate_boards_from_moves(board, move)[0]["board"]
    return new_board, 