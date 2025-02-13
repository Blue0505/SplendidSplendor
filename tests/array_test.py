import unittest

import numpy as np

from splendor.gem import Gem
from splendor.card import Card
from splendor.board import Board
from splendor.player import Player


class TestArrayMethods(unittest.TestCase):
    def test_card_array(self):
        arr = np.array(Card(0, Gem.RED, (3, 0, 0, 0, 0)))
        self.assertTrue(np.array_equal(arr, [0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0]))
        arr = np.array(Card(5, Gem.RED, (0, 0, 7, 3, 0)))
        self.assertTrue(np.array_equal(arr, [5, 0, 0, 0, 1, 0, 0, 0, 7, 3, 0]))
        arr = np.array(Card(5, Gem.GREEN, (0, 7, 3, 0, 0)))
        self.assertTrue(np.array_equal(arr, [5, 0, 0, 1, 0, 0, 0, 7, 3, 0, 0]))
        arr = np.array(Card(5, Gem.WHITE, (3, 0, 0, 0, 7)))
        self.assertTrue(np.array_equal(arr, [5, 1, 0, 0, 0, 0, 3, 0, 0, 0, 7]))
        arr = np.array(Card(5, Gem.BLUE, (7, 3, 0, 0, 0)))
        self.assertTrue(np.array_equal(arr, [5, 0, 1, 0, 0, 0, 7, 3, 0, 0, 0]))
        arr = np.array(Card(5, Gem.BLACK, (0, 0, 0, 7, 3)))
        self.assertTrue(np.array_equal(arr, [5, 0, 0, 0, 0, 1, 0, 0, 0, 7, 3]))

    def test_player_array(self):
        arr = np.array(Player())
        self.assertEqual(len(arr), 45)

    def test_board_array(self):
        arr = np.array(Board("data/cards.csv"))
        self.assertEqual(len(arr), 138)

if __name__ == "__main__":
    unittest.main()
