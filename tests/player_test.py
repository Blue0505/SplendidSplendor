import unittest
import numpy as np
from numpy.typing import NDArray

from splendor_hard.player import Player
from splendor_hard.card import Card 
from splendor_hard.gem import Gem
from splendor_hard.gems import Gems

_TEST_CARD = Card(points=0, gem_type=Gem.BLUE, costs=(5, 5, 5, 5, 5))

def set_resource_array(player: Player, resource_array: NDArray):
    """Helper function that gives a player cards so that they have the amount of resources listed in the
    resource array when `player.get_resource_array()` is called."""
    player._purchased_cards = [] # Reset existing cards. 
    for gem_type, amount in enumerate(resource_array):
        for _ in range(0, amount):
            dummy_card = Card(points=0, gem_type=Gem(gem_type), costs=(0, 0, 0, 0, 0))
            player.add_purchased_card(dummy_card)


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.player = Player()
    
    def tearDown(self) -> None:
        del self.player

    def test_can_purchase(self):
        with self.subTest("Purchase with only resources."):
            set_resource_array(self.player, np.array([10, 6, 10, 5, 10]))
            self.assertTrue(self.player.can_purchase(_TEST_CARD))
    
        with self.subTest("Cannot purchase with resources."):
            set_resource_array(self.player, np.array([2, 6, 10, 5, 10]))
            self.assertFalse(self.player.can_purchase(_TEST_CARD))
        
        with self.subTest("Player has nothing and cost of the card is zero."):
            empty_card = Card(0, Gem.BLACK, (0, 0, 0, 0, 0))
            self.assertTrue(self.player.can_purchase(empty_card))
        
        with self.subTest("Cannot purchase with resource gem combination."):
            set_resource_array(self.player, np.array([2, 6, 10, 5, 10]))
            self.player.gems = Gems(np.array([2, 0, 0, 0, 0, 0]))
            self.assertFalse(self.player.can_purchase(_TEST_CARD))
        
        with self.subTest("Can purchase with resource gem combination."):
            set_resource_array(self.player, np.array([2, 6, 10, 5, 10]))
            self.player._gems = np.array([3, 0, 0, 0, 0]) # 5 - 2 - 3 = 0; just barely enough.
            self.player.gems = Gems(np.array([3, 0, 0, 0, 0, 0]))
            self.assertTrue(self.player.can_purchase(_TEST_CARD))
        
        with self.subTest("Player can only afford due to gold."):
            set_resource_array(self.player, np.array([2, 6, 10, 5, 10]))
            self.player.gems = Gems(np.array([2, 0, 0, 0, 0, 1]))
            self.assertTrue(self.player.can_purchase(_TEST_CARD, using_gold=True))
        
        with self.subTest("Player can afford using only gold."):
            set_resource_array(self.player, np.zeros(5).astype(int))
            self.player.gems = Gems(np.array([0, 0, 0, 0, 0, 25]))
            self.assertTrue(self.player.can_purchase(_TEST_CARD, using_gold=True))


if __name__ == "__main__":
    unittest.main()
