from .gem import Gem
from .card import Card
from numpy.typing import NDArray
import numpy as np

PLAYER_GEMS_START: int = 0
MAX_RESERVE: int = 3

class Player:
    """A player that can have purchased cards, reserved cards, and counts for
    each gem type.
    
    Gems are represented in the following order: White, Blue, Green, Red, Black, (Gold).
    """
    def __init__(self):
        self._gems = np.empty(5).fill(PLAYER_GEMS_START)
        self._gold_gems = PLAYER_GEMS_START
        self._purchased_cards: list[Card] = []
        self._reserved_cards: list[Card] = [] 
 
    def __array__(self): # TODO. 
        pass


    def add_card(self, card: Card) -> None:
        self._purchased_cards.append(card)

    def reserve_card(self, card: Card) -> None:
        self._reserved_cards.append(card)

    def can_reserve(self) -> bool:
        return len(self._reserved_cards) < MAX_RESERVE
    
    def purchase_card(self, card: Card):
        self._purchased_cards.append(card)

    def can_purchase(self, card: Card) -> bool:
        moving_sum: int = 0
        zeros = np.zeros(5)
        gem_sum = card.get_costs() - self.get_gems() - self.get_resources()
        np.clip(gem_sum, amin=0)
        return np.sum(gem_sum) - self._gold_gems <= 0
    

    def get_resources(self):
        """Returns counts of all permanent gems from resource cards."""
        resources = np.empty(5)
        for card in self._purchased_cards:
            resources[card._gem_type] += 1

        return resources
    

    def update_gems(self, white=0, blue=0, green=0, red=0, black=0, gold=0):
        """Add or remove gems from this player."""
        self._gems = self._gems + np.array([white, blue, green, red, black])
        self._gold_gems += gold

    def get_gems(self):
        """Returns the number of gems this player has of each type."""
        return self._gems
    
    def get_gold(self) -> int:
        return self._gold_gems

    def get_points(self):
        return sum(card._points for card in self._purchased_cards)