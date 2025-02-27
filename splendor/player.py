import numpy as np
from numpy.typing import NDArray

from splendor.card import Card
from splendor.gems import Gems, gem_array_str

PLAYER_GEMS_START: int = 0
MAX_RESERVE: int = 3


class Player:
    """A player that can have purchased cards, reserved cards, and counts for
    each gem type.

    Gems are represented in the following order: White, Blue, Green, Red, Black, (Gold).
    """

    def __init__(self):
        self.gems = Gems(np.full((6), PLAYER_GEMS_START))
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

        return (
            f"   Gems: {gem_array_str(self.gems.get_array(), gold=True)}\n"
            f"   {reserved_str}\n"
            f"   Resources: {gem_array_str(self.get_resources_array())}\n"
            f"   Points: {self.get_points()}\n"
        )

    def add_purchased_card(self, card: Card) -> None:
        self._purchased_cards.append(card)
        return None

    def add_reserved_card(self, card: Card) -> None:
        self._reserved_cards.append(card)

    def pop_reserved_card(self, pos: int) -> Card:
        return self._reserved_cards.pop(pos)

    def reserve_limit(self) -> bool:
        return not len(self._reserved_cards) < MAX_RESERVE

    def get_points(self):
        return sum(card._points for card in self._purchased_cards)

    def can_purchase(self, card: Card, using_gold: bool = True) -> bool:
        """Return True if the player can afford a card using their resources, gems, and (optionally) gold."""
        purchase_gems = card.gems.get_array() - self.gems.get_array() - self.get_resources_array()
        purchase_gems = np.clip(purchase_gems, a_min=0, a_max=None)

        if using_gold:
            return np.sum(purchase_gems) - self.gems.get_gold() <= 0
        
        return np.sum(purchase_gems) <= 0

    def get_resources_array(self) -> NDArray:
        """Returns counts of all permanent gems from resource cards."""
        resources = np.zeros(6).astype(int)
        for card in self._purchased_cards:
            resources[card._gem_type] += 1

        return resources

    def get_resources_sum(self) -> int:
        return np.sum(self.get_resources_array())

    def __array__(self) -> NDArray:
        reserved_0 = np.array(self._reserved_cards[0]) if 0 < len(self._reserved_cards) else np.zeros(11)
        reserved_1 = np.array(self._reserved_cards[0]) if 1 < len(self._reserved_cards) else np.zeros(11)  
        reserved_2 = np.array(self._reserved_cards[0]) if 2 < len(self._reserved_cards) else np.zeros(11)  

        return np.array([
            self.get_points(),
            *self.gems.get_array(),
            *self.get_resources_array(),
            *reserved_0,
            *reserved_1,
            *reserved_2
        ])
        
