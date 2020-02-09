'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import piece_movement as PM
import winTester as WT
import math
from random import randint

WHITE_PIECES = 0
BLACK_PIECES = 0

NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7

DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

ZOBRIST_INDEXES = {'p':0, 'P':1, 'c':2, 'C':3, 'l':4, 'L':5, 'i':6, 'I':7,
  'w':8, 'W':9, 'k':10, 'K':11, 'f':12, 'F':13, }
ZOBRIST_NUMBERS = []
ZHASH = None

TRANSPOSITION_TABLE = []
TABLE_SIZE = 0

ALPHA_BETA_CUTOFFS = 0
STATES_EXPANDED = 0
STATIC_EVALS_PERFORMED = 0

INITIAL = BC.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')
initial_state = BC.BC_state(INITIAL)

def makeMove(currentState, currentRemark, timelimit):
    global ALPHA_BETA_CUTOFFS
    ALPHA_BETA_CUTOFFS = 0
    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)
    board = newState.board
    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move
    
    # get zhash value of the current state
    hash = zhash(currentState.board)
    score, newState = minimax(currentState, currentState.whose_move, 2, -100000, 100000, hash)
    #print(score)
    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"
    print(ALPHA_BETA_CUTOFFS)
    print(score)
    print(STATES_EXPANDED)
    print(STATIC_EVALS_PERFORMED)
    return [[newState.prev_move, newState], newRemark]

def nickname():
    return "Newman"

def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."

def prepare(player2Nickname):
    global ZOBRIST_NUMBERS; global TRANSPOSITION_TABLE;  global ZHASH; global TABLE_SIZE
    TRANPOSITION_TABLE = [None] * 1000000
    TABLE_SIZE = len(TRANSPOSITION_TABLE)
    for r in range(8):
        for c in range(8):
            for p in range(14):
                ZOBRIST_NUMBER[r][c][p] == 0
    initZhash()
    ZHASH = zHash(INITIAL)
    pass

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

def update_zhash(location, piece, hash)
    piece = PIECES[piece]
    index = ZOBRIST_INDEXES[piece]
    hash ^= ZOBRIST_NUMBERS[location[0]][location[1]][index]
    return hash

def minimax(state, whoseMove, plyLeft, alpha, beta, hash):
    global ALPHA_BETA_CUTOFFS; global STATES_EXPANDED

    # if plyLeft == 0 or if the state results in a win return its evaluation
    if plyLeft == 0 or WT.winTester(state) != "No win":
        #print(state)
        return (static_eval(state), state)

    if plyLeft > 1:
        if TRANSPOSITION_TABLE[hash % TABLE_SIZE] != None:
            values = get_zhash_values(hash)

    if whoseMove == 1:
        provisional = -100000
    else:
        provisional = 100000
    best_state = state
    #print(len(successors(state, whoseMove)))
    #print(state)

    # recursively go through the successor states
    moves = successors(state,whoseMove)
    next_states = []
    for move in moves:
        new_state = PM.move(move[0], move[1], state, move[2])
        score = static_eval(new_state)
        next_states.append((new_state, score))
    #print(next_states)
    descending = True
    if whoseMove == 0:
        descending = False
    next_states.sort(key=lambda state: state[1], reverse=descending)
    '''for s, score in next_states:
        print(score)
        print(s)
        print("\n")'''
    for s, score in next_states:
        STATES_EXPANDED += 1
        newVal, newS = minimax(s, s.whose_move, plyLeft - 1, alpha, beta)
        if (whoseMove == 1 and newVal > provisional) \
            or (whoseMove == 0 and newVal < provisional):
            if whoseMove == 1:
                alpha = newVal
            else:
                beta = newVal
            provisional = newVal
            best_state = s

            # prune off remaining children as the best move has already been found
            if beta <= alpha:
                ALPHA_BETA_CUTOFFS += 1
                break
    return provisional, best_state

def successors(state, whoseMove):
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
    #copy = BC.BC_state(board)
    global STATIC_EVALS_PERFORMED
    STATIC_EVALS_PERFORMED += 1
    board = state.board
    possible_win = WT.winTester(state)
    if possible_win != "No win":
        if possible_win == "Win for WHITE":
            return 10000
        else:
            return -10000
    return evaluate_piece_strength(board, 1) + evaluate_piece_strength(board, 0)\
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
    frozen = False
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and piece % 2 == side:
                if PM.is_frozen((r,c), board, side):
                    frozen = True
                strength += piece_weights(PIECES[piece], side, frozen)
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
    if PM.is_frozen(king_location, board, side):
        score -= 50
    if PM.is_king_in_check(board, king_location, side):
        return score - 500
    else:
        enemy_coordinator = 5
        if side == 1:
            enemy_coordinator = 4
        coordinator_location = PM.get_piece_location(enemy_coordinator, board)
        enemy_king = 13
        if side == 1:
            enemy_king = 12
        enemy_king_location = PM.get_piece_location(enemy_king, board)
        if coordinator_location is not None:
            if coordinator_location[0] == king_location[0]:
                if abs(enemy_king_location[1] - king_location[1]) == 1:
                    score -= 100
                else:
                    score -= 50
            elif coordinator_location[1] == king_location[1]:
                score -= 10
    return score



def piece_weights(piece, side, frozen):
    multiplier = [-1, 1]
    mult = multiplier[side]
    if frozen:
        mult * 0.5
    if piece in ['p''P']:
        return 10 * mult
    if piece in ['l','L']:
        return 30 * mult
    if piece in ['w','W']:
        return 50 * mult
    if piece in ['c', 'C', 'f','F']:
        return 70 * mult
    if piece in ['i', 'I']:
        return 90 * mult
    else:
        return 0


