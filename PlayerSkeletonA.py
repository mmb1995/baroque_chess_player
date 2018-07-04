'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import piece_movement as PM
WHITE_PIECES = 0
BLACK_PIECES = 0
NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7
DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

def makeMove(currentState, currentRemark, timelimit):

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move
    
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    score, newState = minimax(currentState, currentState.whose_move, 2)

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[((0,0), (0,0)), newState], newRemark]

def nickname():
    return "Newman"

def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."

def prepare(player2Nickname):
    global WHITE_PIECES, BLACK_PIECES
    WHITE_PIECES = 16
    BLACK_PIECES = 16
    pass

def minimax(state, whoseMove, plyLeft):
    if plyLeft == 0:
        return (static_eval(state.board), state)
    if whoseMove == 1:
        provisional = -100000
    else:
        provisional = 100000
    best_state = state
    for s in successors(state, whoseMove):
        newVal, newS = minimax(s, s.whose_move, plyLeft - 1)
        if (whoseMove == 1 and newVal > provisional) \
            or (whoseMove == 0 and newVal < provisional):
            provisional = newVal
            best_state = s
    return provisional, best_state

def successors(state, whoseMove):
    board = state.board
    successors = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0 and piece % 2 == whoseMove:
               if not PM.is_frozen((r,c), board, whoseMove):
                   #print(piece)
                   limit = 8
                   if PIECES[piece] in ['p','P']:
                       limit = 3
                   for i in range(limit):
                       new_states = get_moves((r,c), state, i, whoseMove)
                       for new_state in new_states:
                           #print(new_state)
                           successors.append(new_state)
    print(len(successors))
    return successors

def get_moves(location, state, dir, whoseMove):
    successors = []
    dest = PM.get_next_space(location, dir)
    piece = state.board[location[0]][location[1]]
    enemy = 1 - whoseMove
    while dest is not None:
        dest_piece = state.board[[dest[0]]][dest[1]]
        if dest_piece != 0 and dest_piece % 2 == whoseMove: break
        if PIECES[piece] not in ['i', 'I', 'l', 'L', 'k','K']:
            if dest_piece != 0 and dest_piece % 2 == enemy: break
        if PM.can_move(location, dest, state, dir):
            #print(location)
            #print(dest)
            #print("\n")
            new_state = PM.move(location, dest, state, dir)
            successors.append(new_state)
        dest = PM.get_next_space(dest, dir)
        if piece in ['k','K']: break
        #print(dest)
        #print("\n")
    return successors

def static_eval(board):
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != 0:
                side += piece % 2
                score += piece_weights(PIECES[piece],side )
    return score


def piece_weights(piece, side):
    multiplier = [-1, 1]:
    mult = multiplier[side]
    if piece in ['p''P']:
        return 1*mult
    if piece in ['w','W']:
        return 2 * mult
    if piece in ['l','L']:
        return 5 * mult
    if piece in ['c', 'C', 'i','I']:
        return 7 * mult
    if piece in ['i', 'I']:
        return 9 * mult
    else:
        return 0