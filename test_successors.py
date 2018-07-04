import BC_state_etc as BC
import mmb36_Baroque_Agent as agent
import piece_movement as PM
import unittest

INITIAL = BC.parse('''
c l i w k i l f
- p p p p p p p
p - - - - - - -
- - - - - - - -
- - - - - - - -
P - - - - - - -
- P P P P P P P
F L I W K I L C
''')

goal1 = BC.parse('''
- l i w k i l f
c p p p p p p p
p - - - - - - -
- - - - - - - -
- - - - - - - -
P - - - - - - -
- P P P P P P P
F L I W K I L C
''')

board2 = BC.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - P
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P -
F L I W K I L C
''')


board3 = BC.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - P -
P P P P P P - P
F L I W K I L C
''')

board4 = BC.parse('''
c l i w k i l f
p p p p p p p p
- - P - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P - P P P P P
F L I W K I L C
''')



class Test_Successors(unittest.TestCase):

   ''' def test(self):
        test1 = BC.BC_state(INITIAL)
        succ = agent.successors(test1, 1)
        print(len(succ))
        for s in succ:
            print(s)
        succ2 = agent.successors(test1, 0)
        print("\n")
        print(len(succ))
        for s in succ2:
            print(s)
        test2 = BC.BC_state(board4)
        succ3 = agent.successors(test2, 1)
        print("\n")
        print(len(succ3))
        for s in succ3:
            print(s)
        print("Done with test")

    def test2(self):
        test1 = BC.BC_state(INITIAL, 0)
        copy = BC.BC_state(INITIAL, 0)
        goal = BC.BC_state(goal1, 1)
        result_state = PM.move((0,0), (1,0), test1, 1)
        self.assertTrue(test1 == copy)
        self.assertTrue(result_state == goal)
        print(result_state)
        print("tests passed")'''

   def test3(self):
       score = agent.static_eval(board4)
       white_moves = agent.mobility(board4, 1)
       black_moves = agent.mobility(board4, 0)
       white_weight = agent.evaluate_piece_strength(board4, 1)
       black_weight = agent.evaluate_piece_strength(board4, 0)
       print(score)
       print(white_moves)
       print(black_moves)
       print(white_weight)
       print(black_weight)

if __name__ == '__main__':
    unittest.main()