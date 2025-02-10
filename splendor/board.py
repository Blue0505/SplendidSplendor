from random import shuffle
import numpy as np

from splendor.card import Card
from splendor.card_importer import csv_import
from splendor.helpers import gem_array_str

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
        """Check for each gem specified that the board has at least that amount."""
        return not np.all(self._gems < np.array([white,blue,green,red,black]))
    
    def has_gold(self):
        return self._gold > 0

    def pop_card(self, row: int, column: int) -> Card:
        """Remove and return the card associated with the specified columns and row."""
        return self._decks[row].pop(-column - 1)
        
    def update_gems(self, white=0, blue=0, green=0, red=0, black=0, gold=0) -> None:
        """Augmented assign the specified colors. """
        self._gems = self._gems + np.array([white, blue, green, red, black])
        self._gold += gold
    
    def get_visible_cards(self):
        """Return the cards that are face up on the board in row-major order."""
        return self._decks[0][-4:] + self._decks[1][-4:] + self._decks[2][-4:] 

    def __array__(self):
        pass 

    def __str__(self) -> str:
        output = ""
        for i, row in enumerate(self._decks):
            output += f"   Deck {i}: ({i}4) | "
            for j, card in enumerate(row[-1:-5:-1]):
                output += f'({i}{j}) {str(card)} | '
            output += "\n"
        output += f"   Gems: {gem_array_str(self._gems, self._gold)}\n"
        return output
