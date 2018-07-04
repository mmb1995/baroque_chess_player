'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import winTester as WT
import piece_movement_no_hashing as PM
import random as r
import time
import math

NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7

DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

ZOBRIST_INDEXES = {'p':0, 'P':1, 'c':2, 'C':3, 'l':4, 'L':5, 'i':6, 'I':7,
  'w':8, 'W':9, 'k':10, 'K':11, 'f':12, 'F':13, }
ZOBRIST_NUMBERS = []

ZHASH_TABLE = []
TABLE_SIZE = 0

WHITE = 1
BLACK = 0

STATIC_EVALS_PERFORMED = 0
STATES_EXPANDED = 0
ALPHA_BETA_CUTOFFS = 0
STATES_EXPANDED = 0

TIME_LIMIT = 0
START_TIME = 0

OPPONENT = None


def makeMove(currentState, currentRemark, timelimit):
    '''agent searches for and then takes the best action it can take from a given position'''
    global TIME_LIMIT; global START_TIME
    TIME_LIMIT = timelimit
    START_TIME = time.time()
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    current_state = BC.BC_state(currentState.board, currentState.whose_move)
    move, score = iterative_alpha_beta(current_state, current_state.whose_move, 2)
    new_state = None
    if move is not None:
        new_state = PM.move(move[0], move[1], currentState, move[2])
    newRemark = get_remark(move, score, current_state.whose_move)
    print(ALPHA_BETA_CUTOFFS)
    print(STATIC_EVALS_PERFORMED)
    print(score)
    return [[move[0:2], new_state], newRemark[0]]


def get_remark(move, score, my_player):
    wins = ["Hahah take that negamax and zobrist hashing I didn't need you after all.",\
            "Oh thank god I thought for sure a trap was waiting.", "haha lowply takes another victim."]
    losses = ["Next time i'll have zobrist hashing and negamax working then we will see who is laughing."\
              "hmm I guess I should try and increase my plys next time.", "I can't say im shocked.",
              "But but I could beat a guy who made random moves I didnt expect to have to actually think.",
              "use hashing they said, order moves they said, iterative deepening, all of it was no help."]
    positive = ["Against all odds it looks like I might actually win this.", \
                "I can see over the horizon and it doesnt look good for you {} ".format(OPPONENT)]
    negative = ["I knew the horizon would get me eventually", "oh so you do actually know what you are doing, lucky me.",\
        "grumble grumble... stupid zobrist hashing if you were working i'd be winning."]
    if score == 1000000 and my_player == WHITE or score == -1000000 and my_player == BLACK:
        return r.choices(wins)
    if score == 1000000 and my_player == BLACK or score == -1000000 and my_player == WHITE:
        return r.choices(losses)
    if score > 0 and my_player == WHITE or score < 0 and my_player == BLACK:
        return r.choices(positive)
    else:
        return r.choices(negative)

def nickname():
    return "Lowply"


def introduce():
    return "Names lowplay I only search a couple moves ahead because thats all the info I need to beat you bud."


def prepare(player2Nickname, show_stats=True):
    global OPPONENT; global ALPHA_BETA_CUTOFFS; global STATIC_EVALS_PERFORMED
    if show_stats:
        ALPHA_BETA_CUTOFFS = 0
        STATIC_EVALS_PERFORMED = 0
    OPPONENT = player2Nickname
    pass



def iterative_alpha_beta(state, whoseMove, ply):
    '''generates a list of successors performs alpha beta search on them and then reorders the moves and searches to
        a deeper ply'''
    alpha = -1000000000
    beta = 1000000000
    best_move = None
    moves = successors(state, state.whose_move)
    scores = []
    score_values = {}
    best_score = None
    for p in range(1, ply):
        if len(score_values) == len(moves):

            # sorts the list of moves based on returned alpha beta scores to try and get an earlier cutoff at the
            # next ply
            moves = sorted(moves, key=lambda score: score_values[move])
        for move in moves:
            new_state = PM.move(move[0], move[1], state, move[2])
            score, next_move = minimax(new_state, new_state.whose_move, p, alpha, beta)
            score_values[move] = score
            if whoseMove == 1:
                if score > alpha:
                    alpha = score
                    best_move = move
                    best_score = alpha
            else:
                if score < beta:
                    beta = score
                    best_move = move
                    best_score = beta
        time_elapsed = time.time() - START_TIME
        time_left = TIME_LIMIT - time_elapsed
        if TIME_LIMIT - time_elapsed < 0.12:
            return best_move, best_score
    return best_move, best_score


def minimax(state, whoseMove, plyLeft, alpha, beta):
    '''coordinates alpha beta minimax search depending on if the max or min player is at the root'''
    best_move = None
    if whoseMove == 1:
        new_score, best_move = alpha_beta_max(state, alpha, beta, plyLeft)
    else:
        new_score, best_move = alpha_beta_min(state, alpha, beta, plyLeft)
    return new_score, best_move

def alpha_beta_max(state, alpha, beta, plyLeft):
    '''performs alph_beta search from the perspective of the max player'''
    global ALPHA_BETA_CUTOFFS
    if plyLeft == 0 or WT.winTester(state) != "No win":
        return static_eval(state), None
    moves = successors(state, WHITE)
    best_move = None
    for move in moves:
        time_elapsed = time.time() - START_TIME
        if TIME_LIMIT - time_elapsed < 0.1:
            break
        new_state = PM.move(move[0], move[1], state, move[2])
        score, next_move = alpha_beta_min(new_state, alpha, beta, plyLeft - 1)
        if score > alpha:
            alpha = score # alpha acts like max in MiniMax
            best_move = move

        # agent ends search as this state will not be reached
        if alpha >= beta:
            ALPHA_BETA_CUTOFFS += 1
            break
    return alpha, best_move

def alpha_beta_min(state, alpha, beta, plyLeft):
    '''Performs alpha_beta search from the perspective of the min player'''
    global ALPHA_BETA_CUTOFFS
    if plyLeft == 0 or WT.winTester(state) != "No win":
        return static_eval(state), None
    moves = successors(state, BLACK)
    best_move = None
    for move in moves:
        #print(move)
        time_elapsed = time.time() - START_TIME
        if TIME_LIMIT - time_elapsed < 0.1:
            break
        new_state = PM.move(move[0], move[1], state, move[2])
        score, next_move = alpha_beta_max(new_state, alpha, beta, plyLeft - 1)
        if score < beta:
            beta = score # beta acts like min in MiniMax
            best_move = move
        if alpha >= beta:
            ALPHA_BETA_CUTOFFS += 1
            break
    return beta, best_move

def order_moves(moves, side, state):
    scores = {}
    for move in moves:
        PM.move(move[0], move[1], state, move[2])
        score = static_eval(state)
        scores[move] = score
    desc = True
    if side == 0:
        desc = False
    sorted(moves, key=lambda move: scores[move], reverse=desc)
    return moves

def successors(state, whoseMove):
    '''generates every legal move available from the current board for the side that is taking its turn'''
    board = state.board
    successors = []
    if WT.winTester(state) != "No win":
        return successors
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and piece % 2 == whoseMove:
               #if not PM.is_frozen((r,c), board, whoseMove):
                   #print(piece)
               limit = 8
               if PIECES[piece] in ['p', 'P']:
                   limit = 4
               for i in range(limit):
                   get_moves((r,c), state, i, whoseMove, successors)
    #shuffle(successors)
    return successors

def get_moves(location, state, dir, whoseMove, successors):
    '''returns all the possible moves an individual piece can make from its positon on the board'''
    dest = PM.get_next_space(location, dir)
    piece = state.board[location[0]][location[1]]
    enemy = 1 - whoseMove
    while dest is not None:
        dest_piece = state.board[dest[0]][dest[1]]
        if dest_piece != 0 and dest_piece % 2 == whoseMove: break
        if PIECES[piece] not in ['i', 'I', 'l', 'L', 'k','K']:
            if dest_piece != 0 and dest_piece % 2 == enemy: break
        if PM.can_move(location, dest, state.board, dir):
            move = (location, dest, dir)
            successors.append(move)
        if piece in ['k', 'K']: break
        dest = PM.get_next_space(dest, dir)
    return successors

def static_eval(state):
    global STATIC_EVALS_PERFORMED
    STATIC_EVALS_PERFORMED += 1
    board = state.board
    possible_win = WT.winTester(state)

    # if this state is a goal state return the winning players score
    # intentionally set to an arbitrary high number to ensure agent makes this move or avoids it if its opponent
    # would win at this state
    if possible_win != "No win":
        if possible_win == "Win for WHITE":
            return 10000000
        else:
            return -10000000
    return (evaluate_piece_strength(board, 1) + evaluate_piece_strength(board, 0))\
             + round(0.1 * mobility(board, 1) - mobility(board, 2))\
             + (king_safety(board, 1) - king_safety(board, 0))

def king_safety(board, side):
    '''Inflicts a heavy penalty if the agent leaves the king vulnerable and pays special attention to enemy coordinator
        due to its unique ability to capture the king without first putting the king into check'''
    score = 0
    king = 12
    if side == 1:
        king = 13
    enemy = 1 - side
    king_location = PM.get_piece_location(king, board)
    if PM.is_frozen(king_location, board, side):
        # a frozen king is more vulnerable to capture
        score -= 100
    if PM.is_king_in_check(board, king_location, side):
        # moves that lead to an agents king being in check should be avoided at all costs
        return score - 1000
    else:

        # the enemy coordinator appears to be the biggest threat to the king as it can eliminate the king without first
        # putting the king in check and also can capture the king even if the king is completly enclosed by friendly
        # pieces
        enemy_coordinator = 5
        if side == 1:
            enemy_coordinator = 4
        coordinator_location = PM.get_piece_location(enemy_coordinator, board)
        enemy_king = 13
        if side == 1:
            enemy_king = 12
        enemy_king_location = PM.get_piece_location(enemy_king, board)

        # the coordinator is more dangerous if it is in the same row as the king as it is unlikely-although possible-
        # that the two kings will find themselves in the same row
        if coordinator_location is not None:
            if coordinator_location[0] == king_location[0]:
                if abs(enemy_king_location[1] - king_location[1]) == 1:
                    score -= 200
                else:
                    score -= 100
            elif coordinator_location[1] == king_location[1]:
                score -= 10
    return score

def evaluate_piece_strength(board, side):
    '''The major factor in the heuristic intended to encourage agent to gain a material advantage over its foe'''
    strength = 0
    frozen = False
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and piece % 2 == side:
                if PM.is_frozen((r,c), board, side):
                    frozen = True
                strength += piece_weights(PIECES[piece], side, frozen)
    return strength

def piece_weights(piece, side, frozen):
    '''Attempts to evaluate the relative values of pieces based on classic chess weights and test game results'''
    multiplier = [-1, 1]
    mult = multiplier[side]

    # pieces lose most of their value if they are frozen and thus unable to move or capture opponents pieces
    if frozen:
        mult * 0.25

    # least valuable piece due to its more limited movement and the fact that it is the most common,
    # although it can capture up to 3 pieces in one move, but this is very difficult to accomplish.
    if piece in ['p''P']:
        return 10 * mult

    # value is harmed due to our rules not allowing double jumping thus costing this piece its most valuable asset
    if piece in ['l','L']:
        return 30 * mult

    # has simplest capture method and is effective at capturing enemy pieces on the edge of the board
    if piece in ['w','W']:
        return 50 * mult

    # the coordinator can capture 2 pieces in one move and can capture the king without putting it into check first
    # the freezer can't capture but can freeze opponents pieces and heavily reduce opponents mobility
    if piece in ['c', 'C', 'f','F']:
        return 70 * mult

    # under our rules could potentially capture 6 pieces in one move, 3 pawns, enemy withdrawer, and enemy coordinator
    if piece in ['i', 'I']:
        return 90 * mult
    else:
        return 0


def mobility(board, side):
    '''intended to encourage movement by the agent especially in earlier turns when material advantage will be equal'''
    enemy = 1 - side
    moves = 0
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if PIECES[piece] != '-' and piece % 2 == side:
                limit = 8
                if PIECES[piece] in ['p','P']:
                    limit = 4
                for i in range(limit):
                    dest = PM.get_next_space((r,c), i)
                    while dest is not None:
                        dest_piece = board[dest[0]][dest[1]]
                        if PIECES[dest_piece] != '-':
                            if dest_piece % 2 == side: break
                            if PIECES[piece] not in ['i','I','l','L','k','K']:
                                if dest_piece % 2 == enemy: break
                        if PM.can_move((r,c), dest, board, i):
                            moves += 1
                        if PIECES[piece] in ['k','K']: break
                        dest = PM.get_next_space(dest, i)
    return moves