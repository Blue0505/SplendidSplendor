import numpy as np
from numpy.typing import NDArray

from splendor.card import Card
from splendor.helpers import gem_array_str

PLAYER_GEMS_START: int = 0
MAX_RESERVE: int = 3

class Player:
    """A player that can have purchased cards, reserved cards, and counts for
    each gem type.
    
    Gems are represented in the following order: White, Blue, Green, Red, Black, (Gold).
    """
    def __init__(self):
        self._gems: NDArray = np.full((5), PLAYER_GEMS_START)
        self._gold_gems = PLAYER_GEMS_START
        self._purchased_cards: list[Card] = []
        self._reserved_cards: list[Card] = []

    def __str__(self):
        reserved_str = "Reserved cards: "
        if not self._reserved_cards:
            reserved_str += "None"
        else:
            reserved_str += "| "
        for r_card in self._reserved_cards: 
            reserved_str += f"{r_card} | "
      
        return (f"   Gems: {gem_array_str(self._gems, self._gold_gems)}\n"
                f"   {reserved_str}\n"
                f"   Resources: {gem_array_str(self.get_resources_array())}\n"
                f"   Points: {self.get_points()}\n")

    def add_purchased_card(self, card: Card) -> None:
        self._purchased_cards.append(card)
        return None

    def add_reserved_card(self, card: Card) -> None:
        self._reserved_cards.append(card)

    def pop_reserved_card(self, pos: int) -> Card:
        return self._reserved_cards.pop(pos)

    def reserve_limit(self) -> bool:
        return not len(self._reserved_cards) < MAX_RESERVE


    def can_purchase(self, card: Card, using_gold: bool = True) -> bool:
        """Return True if the player can afford a card using their resources, gems, and (optionally) gold."""
        purchase_gems: NDArray = card.get_costs_array() - self.get_gems_array() - self.get_resources_array()
        purchase_gems = np.clip(purchase_gems, a_min=0, a_max=None)
        if using_gold:
            return np.sum(purchase_gems) - self._gold_gems <= 0
        return np.sum(purchase_gems)
    
    def get_resources_array(self) -> NDArray:
        """Returns counts of all permanent gems from resource cards."""
        resources = np.zeros(5).astype(int)
        for card in self._purchased_cards:
            resources[card._gem_type] += 1

        return resources
    

    def update_gems(self, white=0, blue=0, green=0, red=0, black=0, gold=0):
        """Add or remove gems from this player."""
        self._gems = self._gems + np.array([white, blue, green, red, black])
        self._gold_gems += gold
    
    def has_gems(self, white=np.nan, blue=np.nan, green=np.nan, red=np.nan, black=np.nan, gold=np.nan) -> bool:
        """Check for each gem specified that the board has at least that amount."""
        return (not np.any(self._gems < np.array([white, blue, green, red, black]))) and (not self._gold_gems < gold)

    def get_gems_array(self):
        return self._gems
    
    def get_gold(self) -> int:
        return self._gold_gems

    def get_points(self):
        return sum(card._points for card in self._purchased_cards)

    def get_sum(self):
        """Return the sum of all the users gems and gold."""
        return np.sum(self._gems) + self._gold_gems
    
    def __array__(self): # TODO. 
        pass