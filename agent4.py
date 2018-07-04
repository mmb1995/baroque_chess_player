'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import winTester as WT
import piece_movement as PM

NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7

DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

WHITE = 1
BLACK = 0

STATIC_EVALS_PERFORMED = 0
STATES_EXPANDED = 0
ALPHA_CUTOFFS = 0
BETA_CUTOFFS = 0

def makeMove(currentState, currentRemark, timelimit):

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = minimax(currentState, currentState.whose_move, 3)
    new_state = None
    if move is not None:
        new_state = PM.move(move[0], move[1], currentState, move[2])
    newRemark = "I'll think harder in some future game. Here's my move"
    print(ALPHA_CUTOFFS)
    print(BETA_CUTOFFS)
    return [[move[0:2], new_state], newRemark]


def nickname():
    return "Newman"


def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."


def prepare(player2Nickname):
    pass


def minimax(state, whoseMove, plyLeft):
    moves = successors(state, whoseMove)
    best_move = None
    for ply in range(1, plyLeft):
        alpha = -100000
        beta = 100000
        for move in moves:
            new_state = PM.move(move[0], move[1], state, move[2])
            if whoseMove == 1:
                new_score = alpha_beta_min(new_state, alpha, beta, ply)
            else:
                new_score = alpha_beta_max(new_state, alpha, beta, ply)
            #print(new_score)
            if whoseMove == 1:
                if new_score > alpha:
                    alpha = new_score
                    best_move = move
            else:
                if new_score < beta:
                    beta = new_score
                    best_move = move
    return best_move

def alpha_beta_max(state, alpha, beta, plyLeft):
    global BETA_CUTOFFS
    if plyLeft == 0 or WT.winTester(state) != "No win":
        return static_eval(state)
    moves = successors(state, WHITE)
    for move in moves:
        new_state = PM.move(move[0], move[1], state, move[2])
        score = alpha_beta_min(new_state, alpha, beta, plyLeft - 1)
        if score > alpha:
            BETA_CUTOFFS += 1
            return beta, None # fail hard beta - cutoff
        if alpha >= beta:
            ALPHA_BETA_CUTOFFS +=1
            break
            alpha = score  # alpha acts like max in MiniMax
    return alpha

def alpha_beta_min(state, alpha, beta, plyLeft):
    global ALPHA_CUTOFFS
    if plyLeft == 0 or WT.winTester(state) != "No win":
        return static_eval(state)
    moves = successors(state, BLACK)
    for move in moves:
        new_state = PM.move(move[0], move[1], state, move[2])
        score = alpha_beta_max(new_state, alpha, beta, plyLeft - 1)
        if score <= alpha:
            ALPHA_CUTOFFS += 1
            return alpha # fail hard alpha - cutoff
        if score < beta:
            beta = score  # beta acts like min in MiniMax
    return beta

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
    return successors

def get_moves(location, state, dir, whoseMove, successors):
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
    if PIECES[state.board[2][7]] == 'P':
        return 100
    else:
        return -100
    board = state.board
    possible_win = WT.winTester(state)
    if possible_win != "No win":
        if possible_win == "Win for WHITE":
            return 10000
        else:
            return -10000
    return evaluate_piece_strength(board, 1) + evaluate_piece_strength(board, 0)\
           + (king_safety(board, 1) - king_safety(board, 0))

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