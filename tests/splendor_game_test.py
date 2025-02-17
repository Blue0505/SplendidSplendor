import unittest
import pyspiel
import numpy as np
import pickle

import splendor_game
from splendor.actions import SCategory, SAction
from splendor.gem import Gem
from splendor.card import Card


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
        game = pyspiel.load_game("python_splendor", {"shuffle_cards": False})
        self.state = game.new_initial_state()
        self.actions = (
            self.state._actions
        )  # For getting actions by category in the tests.

    def tearDown(self):
        del self.state
        del self.actions

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

        VALID_GEMS_BOARD = np.array([4, 3, 3, 4, 4])
        VALID_GOLD_BOARD = 5 - 3  # Start - from reserved.
        self.assertTrue(np.array_equal(VALID_GEMS_BOARD, self.state._board._gems))
        self.assertTrue(self.state._board._gold == VALID_GOLD_BOARD)

        VALID_GEMS_PLAYER = np.array([0, 1, 1, 0, 0])
        VALID_GOLD_PLAYER = 0
        self.assertTrue(
            np.array_equal(VALID_GEMS_PLAYER, self.state._player_1.get_gems_array())
        )
        self.assertTrue(VALID_GOLD_PLAYER == self.state._player_1.get_gold())

        VALID_RESOURCES = np.array([0, 0, 0, 1, 0])
        self.assertTrue(
            np.array_equal(VALID_RESOURCES, self.state._player_1.get_resources_array())
        )

    def test_player_resources(self):
        """Tests that a resources enables a player to purchase a card."""
        self.state._player_0._gems = np.array([2, 0, 0, 1, 0])
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
        self.state._player_0._gems = np.array([5, 0, 3, 1, 0])
        self.state._player_0._gold_gems = 1
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
        VALID_GEMS = np.array([2, 1, 4, 1, 1])
        VALID_GOLD = 1
        self.assertTrue(np.array_equal(self.state._player_0._gems, VALID_GEMS))
        self.assertTrue(self.state._player_0._gold_gems == VALID_GOLD)

    def test_purchase_reserve(self):
        """Tests that the player can purchase a card that they reserved and that it decrements their gems correctly."""
        self.state._player_0._gems = np.array([3, 0, 0, 0, 0])
        self.state.apply_action(SAction.RESERVE_03)
        self.state.apply_action(SAction.RESERVE_01)  # "Random" action.
        self.assertIn(SAction.PURCHASE_RESERVE_0, self.state.legal_actions())
        self.assertFalse(
            set([SAction.PURCHASE_RESERVE_1, SAction.PURCHASE_RESERVE_2])
            & set(self.state.legal_actions())
        )
        self.state._player_0._gold_gems = (
            0  # Forces test to not need to deal with spending turn.
        )
        self.state.apply_action(SAction.PURCHASE_RESERVE_0)
        VALID_GEMS = np.zeros(5)
        VALID_GOLD = 0
        self.assertTrue(np.array_equal(self.state._player_0._gems, VALID_GEMS))
        self.assertTrue(self.state._player_0._gold_gems == VALID_GOLD)
        VALID_RESOURCES = [0, 0, 0, 1, 0]
        self.assertTrue(
            np.array_equal(VALID_RESOURCES, self.state._player_0.get_resources_array())
        )

    def test_spending_turn(self):
        """Tests the spending turn mechanic."""
        self.state._player_0._gems = np.array(
            [3, 4, 2, 0, 4]
        )  # one gold for blue and one for green
        self.state._player_0._gold_gems = 2
        # print_actions(self.state.legal_actions())
        self.assertIn(SAction.PURCHASE_21, self.state.legal_actions())
        self.state.apply_action(SAction.PURCHASE_21)
        LEGAL_ACTIONS = [SAction.CONSUME_GOLD_BLUE, SAction.CONSUME_GOLD_GREEN]
        self.assertTrue(np.array_equal(LEGAL_ACTIONS, self.state.legal_actions()))
        self.state.apply_action(SAction.CONSUME_GOLD_GREEN)
        LEGAL_ACTIONS = [SAction.CONSUME_GOLD_BLUE]
        self.assertTrue(np.array_equal(LEGAL_ACTIONS, self.state.legal_actions()))
        self.state.apply_action(SAction.CONSUME_GOLD_BLUE)
        self.state.apply_action(SAction.END_SPENDING_TURN)
        VALID_GEMS_PLAYER = [0, 0, 0, 0, 1]
        VALID_GOLD_PLAYER = 0
        self.assertTrue(np.array_equal(VALID_GEMS_PLAYER, self.state._player_0._gems))
        self.assertTrue(self.state._player_0._gold_gems == VALID_GOLD_PLAYER)
        self.assertTrue(self.state._cur_player == 1)
    
    def test_reward_initial(self):
        """Tests that both players have zero reward when the game is created."""
        self.assertTrue(np.array_equal(self.state.returns(), [0, 0]))
    
    def test_reward_points(self):
        """Tests that the reward calculation is correct when both players have an arbitrary amount of points."""
        p0_card = Card(5, Gem.BLACK, (0, 0, 0, 0, 0))
        p1_card = Card(2, Gem.RED, (0, 0, 0, 0, 0))
        self.state._player_0._purchased_cards = [p0_card]
        self.state._player_1._purchased_cards = [p1_card]
        returns = self.state.returns()
        VALID_RETURNS_P0 = ( (5 - 2) * splendor_game._REWARD_POINTS_SCALE ) 
        VALID_RETURNS_P1 = -VALID_RETURNS_P0
        VALID_RETURNS = [ VALID_RETURNS_P0, VALID_RETURNS_P1 ]
        self.assertTrue(np.array_equal(returns, VALID_RETURNS))
    
    def test_reward_resources(self):
        """Tests that the reward calculation is correct when a player has some resources."""
        p0_card = Card(0, Gem.BLACK, (0, 0, 0, 0, 0))
        self.state._player_0._purchased_cards = [p0_card]
        VALID_RETURNS = [ splendor_game._REWARD_RESOURCES_SCALE, -splendor_game._REWARD_RESOURCES_SCALE ]
        self.assertTrue(np.array_equal(self.state.returns(), VALID_RETURNS))
    
    def test_reward_win(self):
        """Tests that a player receives the correct reward when wining the game."""
        p0_card = Card(15, Gem.BLACK, (0, 0, 0, 0, 0))
        self.state._player_0._purchased_cards = [p0_card]
        self.state.apply_action(SAction.TAKE2_0) # Random action to trigger game end.
        VALID_RETURNS_P0 = splendor_game._REWARD_WIN_SCALE + splendor_game._REWARD_RESOURCES_SCALE + (15 * splendor_game._REWARD_POINTS_SCALE)
        VALID_RETURNS_P1 = -VALID_RETURNS_P0
        VALID_RETURNS = [ VALID_RETURNS_P0, VALID_RETURNS_P1 ]
        self.assertTrue(np.array_equal(self.state.returns(), VALID_RETURNS))

    def try_full_game(self, filename):
        """Helper function that tests that game state matches given actions loaded from a particular file."""
        with open(filename, "rb") as info:
            while True:
                try:
                    action = pickle.load(info)
                    legal_actions = pickle.load(info)
                    tensor = pickle.load(info)

                    self.assertTrue(self.state.legal_actions() == legal_actions)
                    self.assertTrue(self.state.observation_tensor() == tensor)

                    self.state.apply_action(action)

                except EOFError:
                    break 

    # def test_full_game_example(self):
    #     self.test_full_game("tests/playouts/example.pkl")

        


if __name__ == "__main__":
    unittest.main()
