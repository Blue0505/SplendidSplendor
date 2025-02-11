import unittest
import pyspiel

import splendor_game
from splendor.actions import SCategory, Actions, SAction
from splendor.engine import register_splendor_actions

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
        valid = ( self.actions.get_action_ids(SCategory.TAKE2) +
                 self.actions.get_action_ids(SCategory.TAKE3) + 
                 self.actions.get_action_ids(SCategory.RESERVE) ) 
        valid.sort()
        self.assertListEqual(valid, self.state.legal_actions())
    
    def test_max_reserve(self):
        """Test that a player cannot reserve more than three cards."""
        player0_actions = [SAction.RESERVE_00, SAction.RESERVE_00, SAction.RESERVE_00]
        player1_actions = [SAction.TAKE3_00111, SAction.TAKE3_00111, SAction.TAKE3_00111] # "Random" actions.
        apply_actions(self.state, player0_actions, player1_actions)
        reserve_actions = self.actions.get_action_ids(SCategory.RESERVE)
        legal_actions = self.state.legal_actions()
        self.assertFalse(set(reserve_actions) & set(legal_actions))


        






if __name__ == "__main__":
    unittest.main()
