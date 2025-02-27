from random import shuffle
import numpy as np

from splendor.card import Card
from splendor.card_importer import csv_import
from splendor.helpers import gem_array_str
from splendor.gems import Gems

BOARD_COLOR_START: int = 4
BOARD_GOLD_START: int = 5
MAX_RESERVE: int = 3
MIN_DECK_CARDS: int = 5


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
        self.gems = Gems(np.array([BOARD_COLOR_START, BOARD_COLOR_START, BOARD_COLOR_START, BOARD_COLOR_START, BOARD_COLOR_START, BOARD_GOLD_START]))

        self._decks: list[list[Card]] = csv_import(filepath)
        if shuffle_cards:
            for deck in self._decks:
                shuffle(deck)


    def __array__(self):
        return np.concatenate([
            self.gems.get_array(),
            *self._decks[0][-4:],
            *self._decks[1][-4:],
            *self._decks[2][-4:],
        ])


    def __str__(self) -> str:
        output = ""
        for i, row in enumerate(self._decks):
            output += f"   Deck {i}: ({i}0) | "
            for j, card in enumerate(row[-4:]):
                output += f"({i}{j + 1}) {str(card)} | "
            output += "\n"
        output += f"   Gems: {gem_array_str(self.gems.get_array(), gold=True)}\n"
        return output


    def enough_cards(self):
        return (len(self._decks[0]) >= MIN_DECK_CARDS and
                len(self._decks[1]) >= MIN_DECK_CARDS and
                len(self._decks[2]) >= MIN_DECK_CARDS)
    

    def pop_card(self, row: int, col: int) -> Card:
        """Remove and return the card associated with the specified columns and row."""
        return self._decks[row].pop(-4 + (col - 1))


    def get_visible_cards(self):
        """Return the cards that are face up on the board in row-major order."""
        return self._decks[0][-4:] + self._decks[1][-4:] + self._decks[2][-4:]