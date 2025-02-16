import unittest
import numpy as np

from splendor.board import Board


_RANDOM_BOARD = [10, 3, 22, 1, 7]
_RANDOM_GOLD = 5

class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board("data/cards.csv", shuffle_cards=False)

    def test_has_gems(self):
        with self.subTest("Board all zeros; query all zeros."):
            test_query = (0, 0, 0, 0, 0, 0)
            self.board._gems = np.array([0, 0, 0, 0, 0])
            self.board._gold = 0
            self.assertTrue(self.board.has_gems(*test_query))
        
        with self.subTest("Board all zeros; query 1 gold."):
            test_query = (0, 0, 0, 0, 0, 1)
            self.board._gems = np.array([0, 0, 0, 0, 0])
            self.board._gold = 0
            self.assertFalse(self.board.has_gems(*test_query))
        
        with self.subTest("Board all zeros; query has gold and color gem."):
            test_query = (5, 0, 1, 0, 0, 1)
            self.board._gems = np.array([0, 0, 0, 0, 0])
            self.board._gold = 0
            self.assertFalse(self.board.has_gems(*test_query))

        with self.subTest("Random board; query has enough."):
            test_query = (5, 2, 1, 0, 0, 1)
            self.board._gems = np.array(_RANDOM_BOARD) # [10, 3, 22, 1, 7]. 
            self.board._gold = _RANDOM_GOLD # 5.
            self.assertTrue(self.board.has_gems(*test_query))
        
        with self.subTest("Random board; color gem of query not enough."):
            test_query = (5, 2, 1, 5, 0, 1)
            self.board._gems = np.array(_RANDOM_BOARD) # [10, 3, 22, 1, 7]. 
            self.board._gold = _RANDOM_GOLD # 5.
            self.assertFalse(self.board.has_gems(*test_query))

        with self.subTest("Random board; two color gems of query not enough."):
            test_query = (5, 2, 1, 1000, 0, 1)
            self.board._gems = np.array(_RANDOM_BOARD) # [10, 3, 22, 1, 7]. 
            self.board._gold = _RANDOM_GOLD # 5.
            self.assertFalse(self.board.has_gems(*test_query))
        
        with self.subTest("Random board; all parts of query not enough."):
            test_query = (1000, 1000, 1000, 1000, 1000, 1000)
            self.board._gems = np.array(_RANDOM_BOARD)
            self.board._gold = _RANDOM_GOLD
            self.assertFalse(self.board.has_gems(*test_query))



            



if __name__ == "__main__":
    unittest.main()
   