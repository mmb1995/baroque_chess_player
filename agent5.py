

def alphabeta(position, plyleft, alpha, beta):
"""Returns a tuple (score, bestmove) for the position at the given depth"""
    if plyLeft == 0 or wT.winTester(state):
        return static_eval(state), None
    if state.whose_move == WHITE:
            best_move = None
            moves = successors(state, state.whose_move)
            for move in moves:
                new_state = PM.move(move[0], move[1], state, move[2])
                score, move = alphabeta(new_position, plyLeft - 1, alpha, beta)
                if score > alpha: # white maximizes her score
                    alpha = score
                    bestmove = move
                    if alpha >= beta: # alpha-beta cutoff
                        break
            return (alpha, bestmove)
    else:
    bestmove = None
            for move in position.legal_moves():
                new_position = position.make_move(move)
                score, move = alphabeta(new_position, depth - 1, alpha, beta)
                if score < beta: # black minimizes his score
                    beta = score
                    bestmove = move
                    if alpha >= beta: # alpha-beta cutoff
                        break
            return (beta, bestmove)