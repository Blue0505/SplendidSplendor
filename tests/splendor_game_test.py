import unittest
import pyspiel
import numpy as np
import pickle

import splendor_hard.splendor_game as splendor_game
from splendor_hard.actions import SCategory, SAction
from splendor_hard.gem import Gem
from splendor_hard.gems import Gems
from splendor_hard.card import Card

from open_spiel.python.observation import make_observation

def apply_actions(state, player0_actions, player1_actions):
    """Helper function that applies action to the state."""
    for action0, action1 in zip(player0_actions, player1_actions):
        state.apply_action(action0)
        state.apply_action(action1)


def print_actions(actions):
    for action in actions:
        print(SAction(action).name, sep=", ")


class TestSplendorGame(unittest.TestCase):
    def setUp(self):
        game = pyspiel.load_game("splendor_hard", {"shuffle_cards": False})
        self.state = game.new_initial_state()
        self.actions = (
            self.state._actions
        )  # For getting actions by category in the tests.
        self.obs = make_observation(game)

    def tearDown(self):
        del self.state
        del self.actions
        del self.obs

    def test_correct_first_turn(self):
        """Test that the correct actions appear on the first turn."""
        VALID_ACTIONS = (
            self.actions.get_action_ids(SCategory.TAKE2)
            + self.actions.get_action_ids(SCategory.TAKE3)
            + self.actions.get_action_ids(SCategory.RESERVE)
        )
        VALID_ACTIONS.sort()
        self.assertListEqual(VALID_ACTIONS, self.state.legal_actions())

    def test_max_reserve(self):
        """Test that a player cannot reserve more than three cards."""
        player0_actions = [SAction.RESERVE_00, SAction.RESERVE_00, SAction.RESERVE_00]
        player1_actions = [
            SAction.TAKE3_00111,
            SAction.TAKE3_00111,
            SAction.TAKE3_00111,
        ]  # "Random" actions.
        apply_actions(self.state, player0_actions, player1_actions)
        reserve_actions = self.actions.get_action_ids(SCategory.RESERVE)
        legal_actions = self.state.legal_actions()
        self.assertFalse(set(reserve_actions) & set(legal_actions))

    def test_purchase(self):
        """Test that the player and the board have the correct amount of resources/gems after a purchase."""
        player0_actions = [
            SAction.RESERVE_11,
            SAction.RESERVE_11,
            SAction.RESERVE_11,
        ]  # "Random" actions.
        player1_actions = [
            SAction.TAKE3_10110,
            SAction.TAKE3_11010,
            SAction.PURCHASE_02,
        ]
        apply_actions(self.state, player0_actions, player1_actions)

        VALID_GEMS_BOARD = np.array([4, 3, 3, 4, 4, 2])
        # VALID_GOLD_BOARD = 5 - 3  # Start - from reserved.
        self.assertTrue(np.array_equal(VALID_GEMS_BOARD, self.state._board.gems.get_array()))
        # self.assertTrue(self.state._board._gold == VALID_GOLD_BOARD)

        VALID_GEMS_PLAYER = np.array([0, 1, 1, 0, 0, 0])
        self.assertTrue(np.array_equal(VALID_GEMS_PLAYER, self.state._player_1.gems.get_array()))

        VALID_RESOURCES = np.array([0, 0, 0, 1, 0, 0])
        self.assertTrue(np.array_equal(VALID_RESOURCES, self.state._player_1.get_resources_array()))

    def test_player_resources(self):
        """Tests that a resources enables a player to purchase a card."""
        self.state._player_0.gems = Gems(np.array([2, 0, 0, 1, 0, 0]))
        purchase_actions = self.actions.get_action_ids(SCategory.PURCHASE)
        self.assertFalse(set(purchase_actions) & set(self.state.legal_actions()))

        fake_card = Card(0, Gem.RED, (0, 0, 0, 0, 0))
        self.state._player_0.add_purchased_card(fake_card)
        self.assertIn(SAction.PURCHASE_02, self.state.legal_actions())
        self.assertFalse(
            (set(purchase_actions) - set([SAction.PURCHASE_02]))
            & set(self.state.legal_actions())
        )

    def test_player_return_actions(self):
        """Tests the return gems functionality for when a player has more than 10 gems."""
        self.state._player_0.gems = Gems(np.array([5, 0, 3, 1, 0, 1])) 
        self.state.apply_action(SAction.TAKE3_01101)
        return_actions = self.actions.get_action_ids(SCategory.RETURN)
        self.assertTrue(
            (set(return_actions))
            == (set(return_actions)) & set(self.state.legal_actions())
        )  # Ensure all return actions are present.
        self.state.apply_action(SAction.RETURN_0)
        self.state.apply_action(SAction.RETURN_0)
        self.state.apply_action(SAction.RETURN_0)
        self.assertTrue(self.state._cur_player == 1)
        VALID_GEMS = np.array([2, 1, 4, 1, 1, 1])
        self.assertTrue(np.array_equal(self.state._player_0.gems.get_array(), VALID_GEMS))

    def test_purchase_reserve(self):
        """Tests that the player can purchase a card that they reserved and that it decrements their gems correctly."""
        self.state._player_0.gems = Gems(np.array([3, 0, 0, 0, 0, 0]))
        self.state.apply_action(SAction.RESERVE_03)
        self.state.apply_action(SAction.RESERVE_01)  # "Random" action.
        self.assertIn(SAction.PURCHASE_RESERVE_0, self.state.legal_actions())
        self.assertFalse(
            set([SAction.PURCHASE_RESERVE_1, SAction.PURCHASE_RESERVE_2])
            & set(self.state.legal_actions())
        )
        self.state._player_0.gems.get_array()[5] = 0  # Forces test to not need to deal with spending turn.
        
        self.state.apply_action(SAction.PURCHASE_RESERVE_0)
        VALID_GEMS = np.zeros(6)
        self.assertTrue(np.array_equal(self.state._player_0.gems.get_array(), VALID_GEMS))
        VALID_RESOURCES = [0, 0, 0, 1, 0, 0]
        self.assertTrue(
            np.array_equal(VALID_RESOURCES, self.state._player_0.get_resources_array())
        )

    def test_spending_turn(self):
        """Tests the spending turn mechanic."""
        self.state._player_0.gems = Gems(np.array([3, 4, 2, 0, 4, 2]))
        self.assertIn(SAction.PURCHASE_21, self.state.legal_actions())
        self.state.apply_action(SAction.PURCHASE_21)
        LEGAL_ACTIONS = [SAction.CONSUME_GOLD_BLUE, SAction.CONSUME_GOLD_GREEN]
        self.assertTrue(np.array_equal(LEGAL_ACTIONS, self.state.legal_actions()))
        self.state.apply_action(SAction.CONSUME_GOLD_GREEN)
        LEGAL_ACTIONS = [SAction.CONSUME_GOLD_BLUE]
        self.assertTrue(np.array_equal(LEGAL_ACTIONS, self.state.legal_actions()))
        self.state.apply_action(SAction.CONSUME_GOLD_BLUE)
        self.state.apply_action(SAction.END_SPENDING_TURN)
        VALID_GEMS_PLAYER = [0, 0, 0, 0, 1, 0]
        self.assertTrue(np.array_equal(VALID_GEMS_PLAYER, self.state._player_0.gems.get_array()))
        self.assertTrue(self.state._cur_player == 1)
    
    def test_reward_initial(self):
        """Tests that both players have zero reward when the game is created."""
        self.assertTrue(np.array_equal(self.state.returns(), [0, 0]))
        

if __name__ == "__main__":
    unittest.main()
