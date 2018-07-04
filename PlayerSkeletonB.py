'''PlayerSkeletonB.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import random
import winTester as WT
import piece_movement_no_hashing as PM

NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7
DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

def makeMove(currentState, currentRemark, timelimit):

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    #newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    #newState.whose_move = 1 - currentState.whose_move
    
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    moves = successors(currentState, currentState.whose_move)
    return_move = None
    new_state = None
    if len(moves) != 0:
        move = random.choice(moves)
        new_state = PM.move(move[0], move[1], currentState, move[2])
        return_move = move
    # Make up a new remark
    newRemark = "You like that? I bet you didnt see that coming with all your fancy algorithms."
    return [[move[0:2], new_state], newRemark]


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


def nickname():
    return "Random"

def introduce():
    return "I'm Random Playah. I just randomly pick moves and don't care about strategy. It would be a shame if you lost to me."

def prepare(player2Nickname):
    pass


