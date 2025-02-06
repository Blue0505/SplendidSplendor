from .constants import Gem
from .card import Card

PLAYER_GEMS_START: int = 0
MAX_RESERVE: int = 3

class Player:
    """A player that can have purchased cards, reserved cards, and counts for each gem type."""
    def __init__(self):
        self._white_gems = PLAYER_GEMS_START
        self._blue_gems = PLAYER_GEMS_START
        self._green_gems = PLAYER_GEMS_START
        self._red_gems = PLAYER_GEMS_START
        self._black_gems = PLAYER_GEMS_START
        self._gold_gems = PLAYER_GEMS_START
        self._purchased_cards: list[Card] = []
        self._reserved_cards: list[Card] = [] 
 
    def __array__(self): # TODO
        pass


    def add_card(self, card: Card) -> None:
        self._purchased_cards.append(card)


    def reserve_card(self, card: Card) -> None:
        # TODO: Add gold gem
        self._reserved_cards.append(card)


    def purchase_reserved(self, index: int):
        # TODO: Take gems away
        card: Card = self._reserved_cards[index]
        self._white_gems -= card.white_cost
        self._blue_gems -= card.blue_cost
        self._green_gems -= card.green_cost
        self._red_gems -= card.red_cost
        self._black_gems -= card.black_cost

        self._purchased_cards.append(self._reserved_cards[index])
        del self._reserved_cards[index]


    def can_reserve(self) -> bool:
        return len(self._reserved_cards) < MAX_RESERVE
    
    def purchase_card(self, card: Card):
        # TODO: Take gems away and tell board to take card
        self._purchased_cards.append(card)

    def can_purchase(self, card: Card) -> bool:
        # TODO: Subtract gems from resouce cards
        if self._white_gems < card.white_cost: return False
        elif self._blue_gems < card.blue_cost: return False
        elif self._green_gems < card.green_cost: return False
        elif self._red_gems < card.red_cost: return False
        elif self._black_gems < card.black_cost: return False
        return True
    
    def update_gems(self, white=0, blue=0, green=0, red=0, black=0, gold=0):
        self._white_gems += white
        self._blue_gems += blue
        self._green_gems += green
        self._red_gems += red
        self._black_gems += black
        self._gold_gems += gold
    
    def get_gems(self) -> dict[Gem, int]:
        return {
            Gem.WHITE: self._white_gems,
            Gem.BLUE: self._blue_gems,
            Gem.GREEN: self._green_gems,
            Gem.RED: self._red_gems,
            Gem.BLACK: self._black_gems,
            Gem.GOLD: self._gold_gems
        }
                                                            
    def get_points(self):
        return sum(card.points for card in self._purchased_cards)