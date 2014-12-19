import unittest
from battleship import *


class BattleshipTestCase(unittest.TestCase):

    def setUp(self):
        '''Set up a Battleship object'''

        self.init = Battleship(3)

    def tearDown(self):
        '''Clean up'''

        self.init = None

    def testGridInputText(self):
        '''Test if error raise by invalid input '''

        self.assertRaises(InputError, Battleship, 'three by three')

    def testGridInputNegInt(self):
        '''Test if error raise by invalid negative input '''
        self.assertRaises(InputError, Battleship, -3)

    def testGameBoard(self):
        '''Test if Battleship board created have the correct size '''

        self.assertEqual(len(self.init.p1_grid), 9, "Incorrect board size")

    def testPlaceShip(self):
        '''Test if correct amount of ship placed on grid '''

        self.init.place_ships(self.init.p1_grid, 3)
        count = 0
        for item in self.init.p1_grid.values():
            if item == 'X':
                count += 1
        self.assertEqual(count, 3, "Number of ships placed is incorrect")

    def testShipCount1(self):
        '''Test if count of boat sunk is correct when no ship is "Hit" '''

        self.init.place_ships(self.init.p1_grid, 2)
        self.assertEqual(self.init.human_count, 0,\
                         "Count of ship sunk incorrect")

    def testShipCount2(self):
        '''Test if count of boat sunk is correct '''

        self.init.place_ships(self.init.c_grid, 3)
        for i in range(3):
            for k in range(3):
                coord = '%s, %s' % (i, k)
                self.init.human_move(coord)
        self.assertEqual(self.init.human_count, 3, \
                         "Count of ship sunk incorrect")

    def testCorrectCoord1(self):
        '''Test is error raised when invalid string coordinate inputed '''

        self.assertRaises(InputError, self.init.human_move, 'one, zero')

    def testCorrectCoord2(self):
        '''Test is error raised when invalid list coordinate inputed '''

        self.assertRaises(InputError, self.init.human_move, [2, 2])

    def testCorrectCoord3(self):
        '''Test is error raised when invalid negative coordinate inputed '''

        self.assertRaises(InputError, self.init.human_move, '-1, -2')

    def testNegShipInput(self):
        '''Test if error raised when negative amount of ships entered'''

        self.assertRaises(InputError, self.init.pick_ships, -1, -1, -1, -1)

    def testInvaldShipInput(self):
        '''Test if error raised when invalid string entry entered for
        number of ship '''

        self.assertRaises(InputError, self.init.pick_ships,\
                          'one', 'one', 'one', 'one')


class BattleshipTestCase2(unittest.TestCase):

    def setUp(self):
        '''Set up a Battleship object'''

        self.init = Battleship(3)
        for i in range(3):
            self.init.place_ships(self.init.p2_grid, 3)
            self.init.place_ships(self.init.c_grid, 3)
            self.init.place_ships(self.init.p1_grid, 3)

    def tearDown(self):
        '''Clean up'''

        self.init = None

    def testPlayerMove(self):
        '''Test if player1_move method works correctly '''

        for i in range(3):
            for k in range(3):
                coord = '%s, %s' % (i, k)
                self.init.player1_move(coord)
        self.assertEqual(self.init.p1_count, 9,\
                         "Users coord. input not deal with correctly")

    def testShipOverlap(self):
        '''Test if Battleship creates any overlapping of ships when placing
        them'''

        count = 0
        for item in self.init.c_grid.values():
            if item == 'X':
                count += 1

        self.assertEqual(count, 9, "Ships placed have overlapping")

    def testCompMove(self):
        '''Test if comp_move method works correctly '''

        for i in range(9):
            self.init.comp_move()
        self.assertEqual(self.init.comp_count, 9,\
                         "Computer did not make move accordingly")

    def testHumanMove(self):
        '''Test if human_move method works correctly '''

        for i in range(3):
            for k in range(3):
                coord = '%s, %s' % (i, k)
                self.init.human_move(coord)
        self.assertEqual(self.init.human_count, 9,\
                         "Users coord. input not deal with correctly")

if __name__ == '__main__':
    unittest.main()
