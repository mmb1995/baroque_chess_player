import BC_state_etc as bsc
NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7
DIRECTIONS = [(-1,0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def get_next_space(location, Direction):
    r = location[0] + direction[0]
    c = location[1] + direction[1]
    if r, c in [-1, 8]:
        return None:
    return (r, c)

def who(piece):
    return piece % 2

def is_adjacent_to_enemy(piece_location, board):
    piece = board[piece_location[0]][piece_location[1]]
    piece_side = who(piece)
    enemy = 1 - piece_side
    for d in DIRECTIONS:
        adj_space = get_next_space(piece_location, d)
        if adj_space is None:
            continue
        if board[adj_space[0]][adj_space[1]] % 2 == enemy:
            return True:
    return False


def pincer_capture(pincer_location, board)
    pincer_side = who(board[pincer_location[0]][pincer_location[1]])
    enemy = 1 - pincer_side
    for i in range(4):
        dir = DIRECTIONS[i]
        next = get_next_space(pincer_location, dir)
        if next is None or board[next[0]][next[1]] % 2 != enemy:
            continue
        next = get_next_space(next, dir)
        if next is not None and board[next[0]][next[1]] % 2 == who:
            return True
    return False

def leaper_capture(leaper_location, leaper_destination)
    return None




