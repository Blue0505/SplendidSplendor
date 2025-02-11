import unittest
import pyspiel
import numpy as np

import splendor_game
from splendor.actions import SCategory, Actions, SAction
from splendor.engine import register_splendor_actions
from splendor.gem import Gem
from splendor.card import Card

def apply_actions(state, player0_actions, player1_actions):
    """Helper function that applies action to the state."""
    for action0, action1 in zip(player0_actions, player1_actions):
        state.apply_action(action0)
        state.apply_action(action1)


class TestSplendorGame(unittest.TestCase):
    def setUp(self):
        game = pyspiel.load_game("python_splendor", {"shuffle_cards": False})
        self.state = game.new_initial_state()
        self.actions = Actions()
        register_splendor_actions(self.actions)
    
    def tearDown(self):
        del self.state
        del self.actions
    
    def test_correct_first_turn(self):
        """Test that the correct actions appear on the first turn."""
        VALID_ACTIONS = ( self.actions.get_action_ids(SCategory.TAKE2) +
                 self.actions.get_action_ids(SCategory.TAKE3) + 
                 self.actions.get_action_ids(SCategory.RESERVE) ) 
        VALID_ACTIONS.sort()
        self.assertListEqual(VALID_ACTIONS, self.state.legal_actions())
    
    def test_max_reserve(self):
        """Test that a player cannot reserve more than three cards."""
        player0_actions = [SAction.RESERVE_00, SAction.RESERVE_00, SAction.RESERVE_00]
        player1_actions = [SAction.TAKE3_00111, SAction.TAKE3_00111, SAction.TAKE3_00111] # "Random" actions.
        apply_actions(self.state, player0_actions, player1_actions)
        reserve_actions = self.actions.get_action_ids(SCategory.RESERVE)
        legal_actions = self.state.legal_actions()
        self.assertFalse(set(reserve_actions) & set(legal_actions))

    def test_purchase(self):
        """Test that the player and the board have the correct amount of resources/gems after a purchase."""
        player0_actions = [SAction.RESERVE_11, SAction.RESERVE_11, SAction.RESERVE_11] # "Random" actions.
        player1_actions = [SAction.TAKE3_10110, SAction.TAKE3_11010, SAction.PURCHASE_02]
        apply_actions(self.state, player0_actions, player1_actions)

        VALID_GEMS_BOARD = np.array([4, 3, 3, 4, 4])
        VALID_GOLD_BOARD = 5 - 3 # Start - from reserved.
        self.assertTrue(np.array_equal(VALID_GEMS_BOARD, self.state._board._gems))
        self.assertTrue(self.state._board._gold == VALID_GOLD_BOARD)

        VALID_GEMS_PLAYER = np.array([0, 1, 1, 0, 0])
        VALID_GOLD_PLAYER = 0
        self.assertTrue(np.array_equal(VALID_GEMS_PLAYER, self.state._player_1.get_gems_array()))
        self.assertTrue(VALID_GOLD_PLAYER == self.state._player_1.get_gold())

        VALID_RESOURCES = np.array([0, 0, 0, 1, 0])
        self.assertTrue(np.array_equal(VALID_RESOURCES, self.state._player_1.get_resources_array()))
    
    def test_player_resources(self):
        """Tests that a resources enables a player to purchase a card."""
        self.state._player_0._gems = np.array([2, 0, 0, 1, 0])
        purchase_actions = self.actions.get_action_ids(SCategory.PURCHASE)
        self.assertFalse(set(purchase_actions) & set(self.state.legal_actions()))

        fake_card = Card(0, Gem.RED, (0, 0, 0, 0, 0))
        self.state._player_0.add_purchased_card(fake_card)
        self.assertIn(SAction.PURCHASE_02, self.state.legal_actions())
        self.assertFalse((set(purchase_actions) - set([SAction.PURCHASE_02])) & set(self.state.legal_actions()))
        

        






if __name__ == "__main__":
    unittest.main()
