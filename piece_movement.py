import BC_state_etc as bcs
import zobrist as Z

NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7
OPP_DIRECTIONS = [1, 0, 3, 2, 7, 6, 5, 4]
DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

def who(piece):
    return piece % 2

def is_frozen(location, board, side):
    enemy = 1 - side
    enemy_freezer = 15
    if enemy == 0:
        enemy_freezer = 14
    for i in range(8):
        next = get_next_space(location, i)
        if next is not None:
            next_piece = board[next[0]][next[1]]
            if next_piece == enemy_freezer:
                return True
    return False

def get_next_space(location, direction):
    dir = DIRECTIONS[direction]
    r = location[0] + dir[0]
    c = location[1] + dir[1]
    if r in [-1, 8] or c in [-1, 8]:
        return None
    return (r, c)

def can_move(start_pos, dest, board, dir):
    if  dest[0] in [-1, 8] or dest[1] in [-1,8]:
            return False
    piece = board[start_pos[0]][start_pos[1]]
    if PIECES[piece] == '-': return False
    side = piece % 2
    enemy = 1 - side
    if is_frozen(start_pos,board,side): return False
    return check_move(start_pos, dest, piece, board, side, enemy, dir)

def move(start_pos, dest, state, dir):
    board = state.board
    #print(state.hash)
    piece = board[start_pos[0]][start_pos[1]]
    whose_move = state.whose_move
    new_state = bcs.BC_state(board, 1 - whose_move, state.hash)
    #print(new_state.hash)
    new_state.board = update_board(start_pos, dest, new_state, piece, dir, whose_move)
    #new_state.whose_move = 1 - whose_move
    return new_state

def update_board(start, dest, state, piece, dir, whose_move):
    new_board = state.board
    new_board = remove_captured_pieces(start, dest, state, piece, dir, whose_move)
    new_board[start[0]][start[1]] = 0
    new_board[dest[0]][dest[1]] = piece
    state.hash = Z.update_zhash_piece_movement(start, dest, piece, state.hash)
    return new_board

def remove_captured_pieces(start, dest, state, piece, dir, whose_move):
    board = state.board
    capture_space = None
    #print(hash)
    if PIECES[piece] in ['p', 'P']:
        captured_pieces = pincer_capture(dest, board, whose_move)
        if captured_pieces is not None:
            for spaces in captured_pieces:
                state.hash = Z.update_zhash_remove_piece(spaces,board[spaces[0]][spaces[1]], state.hash)
                board[spaces[0]][spaces[1]] = 0
    elif PIECES[piece] in ['l', 'L']:
        line = get_line(start, dest, board, dir)
        if leaper_can_capture(line, whose_move, 1 - whose_move):
            capture_space = leaper_capture_space(start, dest, board, dir, whose_move)
    elif PIECES[piece] in ['w', 'W']:
        capture_space = is_adjacent_to_enemy(start, board, whose_move, dir)
    elif PIECES[piece] in ['i', 'I']:
        captured_pieces = chameleon_captures(start, dest, board, whose_move, dir)
        for spaces in captured_pieces:
            state.hash = Z.update_zhash_remove_piece(spaces, board[spaces[0]][spaces[1]], state.hash)
            board[spaces[0]][spaces[1]] = 0
    elif PIECES[piece] in ['c', 'C']:
        captured = coordinator_capture(dest, board, whose_move)
        if captured is not None:
            for c in captured:
                state.hash = Z.update_zhash_remove_piece(c, board[c[0]][c[1]], state.hash)
                board[c[0]][c[1]] = 0
    if capture_space is not None:
        state.hash = Z.update_zhash_remove_piece(capture_space, board[capture_space[0]][capture_space[1]], state.hash)
        board[capture_space[0]][capture_space[1]] = 0
    return board


def get_line(start, dest, board, dir):
    line = []
    current_pos = start
    while current_pos != dest:
        next = get_next_space(current_pos, dir)
        if next is None: return None # if proposed move goes off the game board or ends in atate\
        #  that can't be reached in given direction
        line.append(board[next[0]][next[1]])
        current_pos = next
    return line

def check_move(start, dest, piece, board, side, enemy, dir):
    piece = PIECES[piece]
    line = get_line(start, dest, board, dir)
    if line == None: return False
    if piece not in ['l', 'L', 'k', 'K', 'i','I']:
        if piece in ['p', 'P'] and dir > 3: return False
        return line_is_empty(line)
    elif piece in ['k', 'K']:
        if len(line) != 1:
            return False
        if line[0] == 0: return True
        elif line[0] % 2 == side: return False
        return is_king_in_check(board, dest, side)
    elif piece in ['l', 'L']:
        if line_is_empty(line):
            return True
        return leaper_can_capture(line, side, enemy)
    else:
        king = 12
        if side == 0:
            king = 13
        if line_is_empty(line)\
                or PIECES[line[0]] == king and len(line) == 1\
                or leaper_can_capture(line, side, enemy, True):
            return True
        return False

def leaper_can_capture(line, side, enemy, is_imitator=False):
    if len(line) < 2 or PIECES[line[-1]] != '-':
        return False
    enemy_leaper = None
    if is_imitator:
        enemy_leaper = 'l'
        if side == 0:
            enemy_leaper = 'L'
    for i in range(len(line)):
        p = line[i]
        #print(p)
        if p != 0:
            if p % 2 == side:
                return False # leaper can not leap over its own pieces
            if p % 2 == enemy:
                if is_imitator:
                    if PIECES[p] != enemy_leaper: return False # imitator can only use leaper capture method against leapers
                if (i == len(line) - 1) or (len(line) - 1 > i + 1) or (line[i + 1] != 0):
                    return False # The next space must be open and leaper must stop on an empty space after enemy piece
                return True
    return False # all spaces are empty so no pieces to capture

def leaper_capture_space(start, dest, board, dir, whose_side):
    next = get_next_space(start, dir)
    enemy = 1 - whose_side
    while next != dest:
        #print(next)
        piece = board[next[0]][next[1]]
        if piece != 0 and piece % 2 == enemy:
            #print(next)
            return next
        next = get_next_space(next, dir)
        #print(next)
    return None

def line_is_empty(line):
    for p in line:
        if PIECES[p] != '-':
            return False
    return True

def is_king_in_check(board, king_pos, side):
    '''returns if the king is currently in check'''
    enemy = 1 - side
    for i in range(8):
        next = get_next_space(king_pos, i)
        if next == None: continue
        piece = board[next[0]][next[1]]
        if piece != 0 and piece % 2 == enemy:
            if PIECES[piece] in ['k', 'K', 'i','I']:
                if not is_frozen(next, board, side):
                    return True
            if PIECES[piece] in ['w', 'W']:
                if is_frozen(next, board, side): continue
                next = get_next_space(next, i)
                if next != None:
                    next_piece = board[next[0]][next[1]]
                    if next_piece == 0:
                        return True
        if piece == 0:
            enemy_leaper = 6
            if side == 0:
                enemy_leaper = 7
            opp_dir = OPP_DIRECTIONS[i]
            next = get_next_space(king_pos, opp_dir)
            while next != None:
                next_piece = board[next[0]][next[1]]
                if next_piece == enemy_leaper:
                    return True
                if next_piece != 0: break
                next = get_next_space(next, opp_dir)
    return False


def pincer_capture(pincer_location, board, pincer_side, is_imitator=False):
    '''returns if the location of the pieces captured by the pincer'''
    enemy = 1 - pincer_side
    pincer_captures = []
    for i in range(4):
        next = get_next_space(pincer_location, i)
        if next is None: continue
        piece = board[next[0]][next[1]]
        if piece != 0 and piece % 2 == enemy:
            if is_imitator:
                if PIECES[piece] not in ['p', 'P']: continue
            last = get_next_space(next, i)
            if last == None: continue
            piece = board[last[0]][last[1]]
            if piece != 0 and piece % 2 == pincer_side:
                pincer_captures.append(next)
    if pincer_captures == []: return None
    return pincer_captures

def is_adjacent_to_enemy(piece_location, board, side, dir, is_imitator=False):
    '''for the withdrawer returns'''
    enemy = 1 - side
    opp_dir = OPP_DIRECTIONS[dir]
    adj_space = get_next_space(piece_location, opp_dir)
    if adj_space is not None:
        adj_piece = board[adj_space[0]][adj_space[1]]
        if adj_piece != 0 and adj_piece % 2 == enemy:
            if is_imitator:
                if PIECES[adj_piece] in ['w', 'W']:
                    return adj_space
            #print(adj_space)
            return adj_space
    return None

def coordinator_capture(coord_pos, board, side, is_imitator=False):
    enemy =  1 - side
    king = 13
    if side == 0:
        king = 12
    king_pos = get_piece_location(king, board)
    coord_row = coord_pos[0]
    coord_column = coord_pos[1]
    king_row = king_pos[0]
    king_column = king_pos[1]
    capture_pos = [(coord_row, king_column), (king_row, coord_column)]
    captured_spaces = []
    for pos in capture_pos:
        piece = board[pos[0]][pos[1]]
        if piece != 0 and piece % 2 == enemy:
            if is_imitator:
                if PIECES[piece] in ['c','C']:
                    return pos
                else: continue
            captured_spaces.append(pos)
    if captured_spaces == []: return None
    return captured_spaces

def get_piece_location(piece, board):
    for r in range(8):
        for c in range(8):
            if board[r][c] == piece:
                return (r,c)
    return None


def chameleon_captures(start_pos, dest, board, side, dir):
    enemy = 1 - side
    captured_pieces = []

    # first see if the chameleon captures a leaper in which case it may not capture any other pieces
    line = get_line(start_pos, dest, board, dir)
    can_capture_leaper = leaper_can_capture(line, side, enemy, True)
    if can_capture_leaper:
        captured_pieces.append(leaper_capture_space(start_pos, dest, board, dir, side))
        return captured_pieces

    withdrawer = is_adjacent_to_enemy(start_pos, board, side, dir, True)
    if withdrawer != None:
        captured_pieces.append(withdrawer)
    #print(captured_pieces)
    if dir < 3:
        pincer = pincer_capture(dest, board, side, True)
        if pincer is not None:
            for spaces in pincer:
                #print(spaces)
                captured_pieces.append(spaces)
    #print(captured_pieces)

    coordinator = coordinator_capture(dest, board, side, True)
    if coordinator is not None:
        captured_pieces.append(coordinator)
    #print(captured_pieces)
    king = 12
    if side == 0:
        king = 13
    king_location = get_piece_location(king, board)
    if king_location is not None:
        d = DIRECTIONS[dir]
        if start_pos[0] + d[0] == dest[0] and start_pos[1] + d[1] == dest[1]\
            and king_location == dest:
            captured_pieces.append(king)
    #print(captured_pieces)
    return captured_pieces





