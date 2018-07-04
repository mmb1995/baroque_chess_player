'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import piece_movement as PM
import winTester as WT
from random import randint
import zobrist as Z

WHITE_PIECES = 0
BLACK_PIECES = 0
NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7
DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}
ALPHA_BETA_CUTOFFS = 0
STATES_EXPANDED = 0
STATIC_EVALS_PERFORMED = 0

ZOBRIST_INDEXES = {'p':0, 'P':1, 'c':2, 'C':3, 'l':4, 'L':5, 'i':6, 'I':7,
  'w':8, 'W':9, 'k':10, 'K':11, 'f':12, 'F':13, }
ZOBRIST_NUMBERS = []
ZHASH = None

TRANSPOSITION_TABLE = []
TABLE_SIZE = 0

class Hash_Entry:
    def __init__(self, key, eval=None, type=None, ply=None, best_move=None):
        self.key = key
        self.eval = eval
        self.type = type
        self.ply = ply
        self.best_move = best_move

def makeMove(currentState, currentRemark, timelimit):
    global ALPHA_BETA_CUTOFFS
    ALPHA_BETA_CUTOFFS = 0
    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    hash = Z.zhash(currentState.board)
    #print(hash)
    current_state = BC.BC_state(currentState.board, currentState.whose_move, hash)
    #print(current_state.hash)
    newState = BC.BC_state(currentState.board)

    board = newState.board
    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    score, move = iterative_deepening_alpha_beta(current_state, current_state.whose_move, 3)
    new_state = PM.move(move[0], move[1], current_state, move[2])
    #print(move)
    move = move[0:2]
    #print(score)
    #print(newState)
    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"
    print(ALPHA_BETA_CUTOFFS)
    print(score)
    print(STATES_EXPANDED)
    print(STATIC_EVALS_PERFORMED)
    return [[move, new_state], newRemark]

def nickname():
    return "Newman"

def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."

def prepare(player2Nickname):
    global ZOBRIST_NUMBERS; global TRANSPOSITION_TABLE; global TABLE_SIZE
    print("hello")
    TRANPOSITION_TABLE = [None] * 1000000
    TABLE_SIZE = len(TRANSPOSITION_TABLE)
    Z.init_zhash()
    print("ok")
    pass


def iterative_deepening_alpha_beta(state, whoseMove, ply):
    alpha = -100000
    beta = 100000
    best_move = None
    for i in range(1, ply):
        score, move = negamax(state, whoseMove, i, alpha, beta)
        best_move = move
    return best_move

def negamax(state, plyLeft, alpha, beta):
    global ALPHA_BETA_CUTOFFS; global STATES_EXPANDED

    # if plyLeft == 0 or if the state results in a win return its evaluation
    if plyLeft == 0 or WT.winTester(state) != "No win":
        return (static_eval(state), state)

    # check hashtable for state information and see if the agent can return stored values instead of searching
    index = state.hash % TABLE_LENGTH
    hash_entry = ZHASH_TABLE[index]
    if hash_entry != None and hash_entry.key = state.hash and hash_entry.ply >= plyLeft:
        if hash_entry.type == 'Exact':
            return hash_entry.eval, hash_entry.best_move
        if hash_entry.type == 'Beta Eval':
            if hash_entry.eval >= beta:
                return hash_entry.eval, hash_entry.best_move
        if hash_entry.type == 'Alpha Eval':
            if hash_entry.eval <= alpha:
                return hash_entry.eval, hash_entry.best_move

    if plyLeft > 1:
        ZHASH_TABLE[index] = hash_entry(state.hash)
    # recursively go through the successor states
    best_move = None
    is_exact = False
    for move in successors(state, whoseMove):
        STATES_EXPANDED += 1
        s = PM.move(move[0], move[1], state, move[2])
        new_value, newS =  -minimax(s, plyLeft - 1, -alpha, -beta)
        if new_value >= beta:
            hash_entry = Hash_entry(index)
            hash_entry.eval = new_value
            hash_entry.ply = plyLeft
            hash_entry.type = 'Beta Eval'
            hash_entry.best_move = best_move
            ZHASH_TABLE[index] = hash_entry
            return value, best_move
        if new_value > alpha:
            alpha = new_value
            best_move = move
            is_exact = True

    # this state has fully evaluated all its children
    hash_entry = Hash_entry(index)
    hash_entry.ply = plyLeft
    if is_exact:
        hash_entry.type = 'Exact'
    else:
        hash_entry.type = 'Alpha Eval'
    hash_entry.eval = alpha
    hash_entry.best_move = best_move
    ZHASH_TABLE[index] = hash_entry
    return alpha, best_move

def successors(state, whoseMove):
    board = state.board
    successors = []
    if WT.winTester(state) != "No win":
        return successors
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and piece % 2 == whoseMove:
               if not PM.is_frozen((r,c), board, whoseMove):
                   #print(piece)
                   limit = 8
                   if PIECES[piece] in ['p', 'P']:
                       limit = 4
                   for i in range(limit):
                       get_moves((r,c), state, i, whoseMove, successors)
    #print(len(successors))
    #print("\n")
    return successors

def get_moves(location, state, dir, whoseMove, successors):
    #successors = []
    dest = PM.get_next_space(location, dir)
    piece = state.board[location[0]][location[1]]
    enemy = 1 - whoseMove
    while dest is not None:
        dest_piece = state.board[dest[0]][dest[1]]
        if dest_piece != 0 and dest_piece % 2 == whoseMove: break
        if PIECES[piece] not in ['i', 'I', 'l', 'L', 'k','K']:
            if dest_piece != 0 and dest_piece % 2 == enemy: break
        if PM.can_move(location, dest, state.board, dir):
            #print(location)
            #print(dest)
            #print("\n")
            move = (location, dest, dir)
            successors.append(move)
            #new_state = PM.move(location, dest, state, dir)
            #successors.append(new_state)
        if piece in ['k', 'K']: break
        dest = PM.get_next_space(dest, dir)
        #print(dest)
        #print("\n")
    return successors

def static_eval(state):
    global STATIC_EVALS_PERFORMED
    STATIC_EVALS_PERFORMED += 1
    if PIECES[state.board[2][7]] =='P':
        return 1000
    else:
        return -100
    #copy = BC.BC_state(board)
    board = state.board
    possible_win = WT.winTester(state)
    if possible_win != "No win":
        if possible_win == "Win for WHITE":
            return 1000
        else:
            return -1000
    return evaluate_piece_strength(board, 1) + evaluate_piece_strength(board, 0)\
           + round(0.25 * (mobility(board, 1) - mobility(board, 0)))\
           + round(0.25 * center_control(board, 1) - center_control(board, 0))\
           + (king_safety(board, 1) - king_safety(board, 0))

def mobility(board, side):
    enemy = 1 - side
    moves = 0
    #copy = BC.BC_state(board, side)
    #print(copy)
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
    #print("\n")
    #print(moves)
    #print(copy)
    return moves


def evaluate_piece_strength(board, side):
    strength = 0
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and piece % 2 == side:
                strength += piece_weights(PIECES[piece], side)
    return strength

def center_control(board, side):
    spaces = 0
    line1 = PM.get_line((3,0), (3,7), board, 3)
    line2 = PM.get_line((4,0), (4,7), board, 3)
    for i in range(3, 5):
        for j in range(8):
            if board[i][j] != 0 and board[i][j] % 2 == side:
                spaces += 5
    return spaces

def king_safety(board, side):
    score = 0
    king = 12
    if side == 1:
        king = 13
    enemy = 1 - side
    king_location = PM.get_piece_location(king, board)
    if PM.is_king_in_check(board, king_location, side):
        return 100
    else:
        for i in range(8):
            next = PM.get_next_space(king_location, i)
            if next == None: continue
            if board[next[0]][next[1]] == 0:
                score -= 2
            elif board[next[0]][next[1]] % 2 == enemy:
                score -= 10
            else:
                score += 2
    return score



def piece_weights(piece, side):
    multiplier = [-1, 1]
    mult = multiplier[side]
    if piece in ['p''P']:
        return 1 * mult
    if piece in ['w','W']:
        return 3 * mult
    if piece in ['l','L']:
        return 5 * mult
    if piece in ['c', 'C', 'f','F']:
        return 7 * mult
    if piece in ['i', 'I']:
        return 9 * mult
    else:
        return 0

def initZhash():
    global ZOBRIST_NUMBERS
    for i in range(8):
        for j in range(8):
            for p in range(14):
                zobristnum[i][j][p] = \
                    randint(0, \
                            4294967296)
def zHash(board):
    global ZOBRIST_NUMBERS
    hash = 0
    for r in range(8):
        for c in range(8):
            piece = PIECES[board[r][c]]
            if piece != '-':
                index = ZOBRIST_INDEXES[piece]
                hash ^= ZOBRIST_NUMBERS[r][c][index]
    return hash

def update_zhash_piece_movement(start, dest, piece, hash):
    piece = PIECES[piece]
    index = ZOBRIST_INDEXES[piece]
    hash ^= ZOBRIST_NUMBERS[start[0]][start[1]][index]
    hash ^= ZOBRIST_NUMBERS[dest[0]][dest[1]][index]
    return hash

def update_zhash_remove_piece(location, piece, hash):
    piece = PIECES[piece]
    index = ZOBRIST_INDEXES[piece]
    hash ^= ZOBRIST_NUMBERS[location[0]][location[1]][index]
    return hash

