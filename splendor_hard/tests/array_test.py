import unittest

import numpy as np
import pyspiel
import splendor_hard.splendor_game as splendor_game

import splendor_hard.board as board

from splendor_hard.card_importer import csv_import
from splendor_hard.gem import Gem
from splendor_hard.card import Card
from splendor_hard.board import Board
from splendor_hard.player import Player

from open_spiel.python.observation import make_observation

decks: list[list[Card]] = csv_import("data/cards.csv")

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
        print(len(arr))
        self.assertEqual(len(arr), 45)

    def test_board_array(self):
        arr = np.array(Board("data/cards.csv"))
        self.assertEqual(len(arr), 138)

    def test_observation_tensor_init(self):
        game = pyspiel.load_game("python_splendor", {"shuffle_cards": False})
        state = game.new_initial_state()
        obs = make_observation(game)
        obs.set_from(state, 0) # type: ignore
        np.testing.assert_array_equal(
            obs.tensor, # type: ignore
            np.concatenate([
                np.zeros(splendor_game._PLAYER_SHAPE),
                np.zeros(splendor_game._PLAYER_SHAPE),
                np.array([board.BOARD_COLOR_START]*5),
                [board.BOARD_GOLD_START],
                *decks[0][-4:],
                *decks[1][-4:],
                *decks[2][-4:],
                np.zeros(splendor_game._CARD_SHAPE)
            ])
        )

    def test_observation_tensor_size(self):
        game = pyspiel.load_game("python_splendor", {"shuffle_cards": False})
        state = game.new_initial_state()
        observation = state.observation_tensor()
        self.assertEqual(len(observation), 239)

    def test_observation_tensor_update(self):
        game = pyspiel.load_game("python_splendor", {"shuffle_cards": False})
        state = game.new_initial_state()
        init_obs = make_observation(game)
        init_obs.set_from(state,0) #type: ignore
        obs = make_observation(game)
        state.apply_action(40)
        obs.set_from(state,0) # type: ignore
        #self.assertEqual(obs.tensor[1], 2) # type: ignore
        self.assertEqual(np.sum(obs.tensor),np.sum(init_obs.tensor)) # type: ignore


        
if __name__ == "__main__":
    unittest.main()
