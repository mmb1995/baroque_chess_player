import BC_state_etc as bcs
import piece_movement as pm
import unittest
INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

BOARD1C = bcs.parse('''
c l i w k i l f
- p p p p p p p
- - - - - - - -
- - c - P - - -
- - - - - - - -
- - - - - - - -
P P P P - P P P
F L I W K I L C
''')


BOARD2C = bcs.parse('''
c l i w k i l f
- p p p p p p p
- - - - - - - -
- - - - c C - -
- - - - - - - P
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD1P = bcs.parse('''
c l i w k i l f
- p p p p p p p
- - - - - - - -
- - - - - C p P
- - - - - - - -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD2P = bcs.parse('''
c l i w k i l f
- p - p - p p p
- - - - - - - -
- - p - - C - P
- - I - - - - -
- - p - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD3P = bcs.parse('''
c l i w k i l f
- p - p - p p p
- - - - - - - -
- - p - - C - P
- - I - - - - -
- - P - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD1W = bcs.parse('''
c l i - k i l f
- p p - p p p p
- - - - - - - -
- - - - w C p P
- - p - - - - -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD2W = bcs.parse('''
c l i - k i l f
- p p - p p p p
- - - - - - - -
- - - - - C p P
- - p - - w - -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD3W = bcs.parse('''
c l i - k i l f
- p p - p p p p
- - - - - - - -
- - - - - c p P
- - p - - - W -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD1I = bcs.parse('''
c l i - k - l f
- p p - p - p p
- - - - - - - -
- - - - - - p P
- - p - C i W -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD2I = bcs.parse('''
c l i - k - l f
- p p - p - p p
- - - - - - - -
- - - - - - p P
- - p P i - W -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD3I = bcs.parse('''
c l i - k - l f
- p p - - c p p
- - - - l - - -
- - - - - - p P
- - p P I - W -
- - - - w - - -
P P P P - P P -
F L I W - K L -
''')

BOARD1K = bcs.parse('''
c l i - k I l f
- p p - p - p p
- - - - - - - -
- - - - - - p P
- - p P i - W -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD2K = bcs.parse('''
c l i - - I l f
- p p k p - p p
- - - - - - - -
- - - L - - p P
- - p P i - W -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

BOARD3K = bcs.parse('''
c l i - - I - f
- p p - p l p p
- - - - k - - -
- - - L - W p P
- - p P i - - -
- - - - - - - -
P P P P - P P -
F L I W K I L -
''')

INITIAL = bcs.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

BOARD_ONE_MOVE = bcs.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - P
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P -
F L I W K I L C
''')

BOARD_TWO_MOVES = bcs.parse('''
c l i w k i l f
p p p p p p - p
- - - - - - p P
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P -
F L I W K I L C
''')

BOARD_WITH_CAPTURES = bcs.parse('''
c l i w k i l f
p p p p p p - p
- - - - - P - P
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P - P -
F L I W K I L C
''')

BOARD_C_CAPTURE1 = bcs.parse('''
c l i w k i l f
p p p p - p - p
- - - - - P - P
- - - - p - - -
- - - - - - - -
- - - - - - - -
P P P P P - P -
F L I W K I L C
''')

BOARD_C_CAPTURE2 = bcs.parse('''
c l i w k i l f
p p p p - p - p
- - - - - P - P
- - - - - - - C
- - - - - - - -
- - - - - - - -
P P P P P - P -
F L I W K I L -
''')

BOARD_L_CAPTURE1 = bcs.parse('''
c l i w k i - f
p p p p - p - p
- - - - - P l P
- - - - - - - -
- - - - C - - -
- - - - - - - -
P P P P P - P -
F L I W K I L -
''')

BOARD_L_CAPTURE2 = bcs.parse('''
c l i w k i - f
p p p p - p - p
- - - - - P - P
- - - - - - - -
- - - - - - - -
- - - l - - - -
P P P P P - P -
F L I W K I L -
''')

BOARD_W_CAPTURE1 = bcs.parse('''
c l i w k i - f
p p p p - p - p
- - - - - P - P
- - - - - - - -
- - - - W - - -
- - - l - - - -
P P P P P - P -
F L I - K I L -
''')

BOARD_W_CAPTURE2 = bcs.parse('''
c l i w k i - f
p p p p - p - p
- - - - - P - P
- - - - - W - -
- - - - - - - -
- - - - - - - -
P P P P P - P -
F L I - K I L -
''')

BOARD_I_CAPTURE1 = bcs.parse('''
c l i w k i - f
p p p p - p - p
- - - - - P - P
- - - - i W - -
- - - - - - - -
- - - - - - - -
P P P P P - P -
F L I - K I L -
''')

BOARD_I_CAPTURE2 = bcs.parse('''
c l i w k i - f
p p p p - p - p
- - - - - P - P
i - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P - P -
F L I - K I L -
''')


class test_can_move_and_captures(unittest.TestCase):
    '''
    def test_can_move(self):
        a = [0, 0, 0, 0]
        self.assertTrue(pm.check_move(a, 2, 0, 1, 3))
        b = [0, 3, 0]
        self.assertTrue(pm.check_move(b, 6, 0, 1, 3))
        c = [0, 3, 0, 0, 3]
        self.assertFalse(pm.check_move(c, 6, 0, 1, 3))
        d = [6, 0]
        self.assertTrue(pm.check_move(d, 9, 1, 0, 3))
        f = [3, 8, 5, 0, 0]
        self.assertFalse(pm.check_move(f, 3, 1, 0, 3))
        g = [12]
        self.assertTrue(pm.check_move(g, 9, 1, 0, 3))
        h = [0, 3, 0]
        self.assertFalse(pm.check_move(h, 8, 0, 1, 3))
        i = [0, 0, 4, 0]
        self.assertFalse(pm.check_move(i, 6, 0, 1, 3))
        j = [0, 0, 5, 0]
        self.assertTrue(pm.check_move(j, 6, 0, 1, 3))
        print("Tests passed")'''

    def test_coordinator_capture(self):
        test1 = bcs.BC_state(BOARD1C, 0)
        result = pm.coordinator_capture((3,2), test1.board, 0)
        self.assertTrue(result == [(3,4)])
        test2 = bcs.BC_state(BOARD2C, 0)
        result = pm.coordinator_capture((3,5), test2.board, 1)
        self.assertTrue(result == [(3,4)])
        print("Coordinator capture Passed")

    def test_pincer_capture(self):
        test1 = bcs.BC_state(BOARD1P, 0)
        result = pm.pincer_capture((3,7),BOARD1P, 1)
        #print(result)
        self.assertTrue(result == [(3,6)])
        test2 = bcs.BC_state(BOARD2P, 0)
        result = pm.pincer_capture((3,2), BOARD2P, 0)
        #print(result)
        self.assertTrue(result == [(4,2)])
        test3 = bcs.BC_state(BOARD3P, 0)
        result = pm.pincer_capture((3,2), BOARD3P, 0)
        #print(result)
        self.assertTrue(result == None)
        print("Test pincer capture passed.")

    def test_withdrawer_capture(self):
        test1 = bcs.BC_state(BOARD1W, 0)
        result = pm.is_adjacent_to_enemy((3,4),BOARD1W, 0, 2)
        self.assertTrue(result == (3,5))
        result = pm.is_adjacent_to_enemy((3,4), BOARD1W, 0, 1)
        self.assertTrue(result == None)
        test2 = bcs.BC_state(BOARD2W, 0)
        result = pm.is_adjacent_to_enemy((4,5), test2.board,0, 1)
        #print(result)
        self.assertTrue(result == (3,5))
        result = pm.is_adjacent_to_enemy((4,5), test2.board, 0, 0)
        #print(result)
        self.assertTrue(result == None)
        test3 = bcs.BC_state(BOARD3W, 0)
        result = pm.is_adjacent_to_enemy((4,6), test3.board, 1, 7)
        self.assertTrue(result == (3,5))
        result = pm.is_adjacent_to_enemy((4,6), test3.board, 1, 4)
        self.assertTrue(result == None)
        result = pm.is_adjacent_to_enemy((4,6), test3.board, 0, 7)
        self.assertTrue(result == None)
        print("test withdrawer capture Passed.")

    def test_imitator_capture(self):
        test1 = bcs.BC_state(BOARD1I, 0)
        result = pm.chameleon_captures((0,5),(4, 5),test1.board, 0, 1)
        self.assertTrue(result == [(4,4)])
        test2 = bcs.BC_state(BOARD2I, 0)
        result = pm.chameleon_captures((4,5),(4,4), test2.board, 0, 2)
        #print(result)
        self.assertTrue(result == [(4,6),(4,3)])
        test3 = bcs.BC_state(BOARD3I, 0)
        result = pm.chameleon_captures((4,4), (1,4), test3.board, 1, 0)
        #print(result)
        self.assertTrue(result == (2,4))
        print("Imitator capture passed.")

    def test_king_in_check(self):
        test1 = bcs.BC_state(BOARD1K,0)
        result = pm.is_king_in_check(test1.board, (0,4), 0)
        self.assertTrue(result == True)
        test2 = bcs.BC_state(BOARD2K, 0)
        result = pm.is_king_in_check(test2.board,(1,3) ,0)
        self.assertTrue(result == True)
        test3 = bcs.BC_state(BOARD3K, 0)
        result = pm.is_king_in_check(test3.board, (2, 4), 0)
        self.assertTrue(result == True)
        test4 = bcs.BC_state(BOARD1P, 0)
        result = pm.is_king_in_check(test4.board, (0,4), 0)
        self.assertTrue(result == False)
        print("Test king is in check passed.")

class test_moves(unittest.TestCase):

    def test_basic_move(self):
        test1 = bcs.BC_state(INITIAL, 1)
        goal1 = bcs.BC_state(BOARD_ONE_MOVE, 0)
        result_state = pm.move((6,7),(2,7),test1,1)
        #print(result_state)
        self.assertTrue(result_state == goal1)
        test2 = bcs.BC_state(BOARD_ONE_MOVE, 0)
        goal2 = bcs.BC_state(BOARD_TWO_MOVES, 1)
        #print(test2.board)
        result_state = pm.move((1,6),(2,6),test2,1)
        #print(result_state)
        self.assertTrue(result_state == goal2)
        print("basic move passed.")

    def test_moves_with_captures(self):
        test1 = bcs.BC_state(BOARD_TWO_MOVES, 1)
        goal1 = bcs.BC_state(BOARD_WITH_CAPTURES, 0)
        result_state = pm.move((6,5), (2,5), test1, 0)
        self.assertTrue(result_state == goal1)
        print("Moves with captures passed")

    def test_moves_with_coordinator_capture(self):
        test1 = bcs.BC_state(BOARD_C_CAPTURE1, 1)
        goal1 = bcs.BC_state(BOARD_C_CAPTURE2, 0)
        result_state = pm.move((7,7), (3,7), test1, 0)
        self.assertTrue(result_state == goal1)
        print("Moves with coordinator capture passed")

    def test_moves_with_leaper_capture(self):
        test1 = bcs.BC_state(BOARD_L_CAPTURE1, 0)
        goal1 = bcs.BC_state(BOARD_L_CAPTURE2, 1)
        self.assertFalse(pm.can_move((2,6),(6,2), test1, 6))
        self.assertTrue(pm.can_move((2,6), (5,3), test1, 6))
        result_state = pm.move((2,6),(5,3), test1, 6)
        #print(result_state)
        self.assertTrue(result_state == goal1)
        print("Moves with leaper capture passed")

    def test_move_with_withdrawer_capture(self):
        test1 = bcs.BC_state(BOARD_W_CAPTURE1, 1)
        goal1 = bcs.BC_state(BOARD_W_CAPTURE2, 0)
        self.assertFalse(pm.can_move((4,4), (2,0), test1, 5))
        self.assertTrue(pm.can_move((4,4), (3,5), test1, 5))
        result_state = pm.move((4,4), (3,5), test1, 5)
        #print(result_state)
        self.assertTrue(result_state == goal1)
        print("Move with withdrawer_capture passed")

    def test_move_with_imitator_capture(self):
        test1 = bcs.BC_state(BOARD_I_CAPTURE1, 0)
        goal1 = bcs.BC_state(BOARD_I_CAPTURE2, 1)
        self.assertTrue(pm.can_move((3,4), (3,0), test1, 2))
        self.assertFalse(pm.can_move((3,4),(4,4), test1, 2))
        result_state = pm.move((3,4), (3,0), test1, 2)
        self.assertTrue(result_state == goal1)
        #print(result_state)
        print("Move with imitator capture passed.")

if __name__ == '__main__':
    unittest.main()