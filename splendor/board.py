from random import shuffle
import numpy as np
import csv

from .card import Card
from .gem import Gem

from .card_importer import csv_import

BOARD_GEM_START: int = 4
BOARD_GOLD_START: int = 5
MAX_RESERVE: int = 3

class Board:
    """A board with three levels of decks and some number of gems in the center.
    
    The internal representation of the board in `self._decks` is as follows: 

                          |  COLUMN n-3  |  COLUMN n-2  |  COLUMN n-2  |  COLUMN n-1
    ----------------------|--------------|--------------|--------------|-------------
    ROW 0 (Level 1 cards) | (Card_n - 4) | (Card_n - 3) | (Card_n - 2) | (Card_n - 1)
    ROW 1 (Level 2 cards) | (Card_n - 4) | (Card_n - 3) | (Card_n - 2) | (Card_n - 1)
    ROW 2 (Level 3 cards) | (Card_n - 4) | (Card_n - 3) | (Card_n-  2) | (Card_n - 1)
    
    Columns n-5 down to column 0 represent cards that are flipped upside down in the deck.
    
    """
    def __init__(self, filepath: str, shuffle_cards: bool = True):
        self._gems = np.full((5), BOARD_GEM_START)
        self._gold = BOARD_GOLD_START
    
        self._decks: list[list[Card]] = csv_import(filepath)
        if shuffle_cards: 
            for deck in self._decks:
                shuffle(deck)
    
    def has_gems(self, white=np.nan, blue=np.nan, green=np.nan, red=np.nan, black=np.nan) -> bool:
        gem_request = np.array([white,blue,green,red,black])
        return not np.all(self._gems < np.array([white,blue,green,red,black]))
    
    def has_gold(self):
        return self._gold > 0

    def pop_card(self, row: int, column: int) -> Card:
        return self._decks[row].pop(-column - 1)


    def update_gems(self, white=0, blue=0, green=0, red=0, black=0, gold=0) -> None:
        self._gems = self._gems + np.array([white, blue, green, red, black])
        self._gold += gold
    
    def get_cards(self):
        return [ card for row in self._decks for card in row ] 

    def __array__(self): # TODO!
        pass 