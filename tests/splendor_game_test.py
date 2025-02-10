import unittest
import pyspiel

import splendor_game
from splendor.actions import SCategory, Actions
from splendor.engine import register_splendor_actions

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
        






if __name__ == "__main__":
    unittest.main()
