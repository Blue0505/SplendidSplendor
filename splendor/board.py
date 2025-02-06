from random import shuffle
import csv

from .card import Card
from .gem import Gem

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
        self._white_gems = BOARD_GEM_START
        self._blue_gems = BOARD_GEM_START
        self._green_gems = BOARD_GEM_START
        self._red_gems = BOARD_GEM_START
        self._black_gems = BOARD_GEM_START
        self._gold_gems = BOARD_GEM_START
    
        self._decks: list[list[Card]] = self._load_cards(filepath)
        if shuffle_cards: 
            for deck in self._decks:
                shuffle(deck)
    
    def has_gems(self, white=None, blue=None, green=None, red=None, black=None, gold=None) -> bool:
        if white != None and self._white_gems < white:
            return False
        elif blue != None and self._blue_gems < blue:
            return False
        elif green != None and self._green_gems < green:
            return False
        elif red != None and self._red_gems < red:
            return False
        elif black != None and self._black_gems < black:
            return False
        elif gold != None and self._gold_gems < gold:
            return False
        return True
    

    def pop_card(self, row: int, column: int) -> Card:
        return self._decks[row].pop(-column - 1)


    
    def update_gems(self, white=0, blue=0, green=0, red=0, black=0, gold=0) -> None:
        self._white_gems += white
        self._blue_gems += blue
        self._green_gems += green
        self._red_gems += red
        self._gold_gems += gold
    
    
    def get_cards(self):
        return [ element for row in self._decks for element in row ] 

    
    def __array__(self): # TODO!
        pass 

    
    def _load_cards(self, filepath: str) -> list[list[Card]]:
        """Loads cards from a CSV file and returns three decks. These decks
        contain all level 1, level 2, and level 3 cards respectively.
        """
        csv_gem_names: dict[str, Gem] = {
            'white': Gem.WHITE,
            'blue': Gem.BLUE,
            'green': Gem.GREEN,
            'red': Gem.RED,
            'black': Gem.BLACK
        }

        decks = [[] for _ in range(3)]
        with open(filepath) as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                points = int(row['points']) if row['points'] else 0
                gem_type = csv_gem_names[row['gem-color']]
                costs = {
                    Gem.WHITE: int(row['c-white']) if row['c-white'] else 0,
                    Gem.BLUE: int(row['c-blue']) if row['c-blue'] else 0,
                    Gem.GREEN: int(row['c-green']) if row['c-green'] else 0,
                    Gem.RED: int(row['c-red']) if row['c-red'] else 0,
                    Gem.BLACK: int(row['c-black']) if row['c-black'] else 0
                    
                }
                decks[int(row['level']) - 1].append(Card(points, gem_type, costs))
        return decks