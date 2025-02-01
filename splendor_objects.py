from enum import Enum
from random import shuffle
import csv

import ansi_escape_codes as ansi

BOARD_GEM_START: int = 4 
BOARD_GOLD_START: int = 5 
PLAYER_GEMS_START: int = 0

class Gem(Enum):
    WHITE = enum.auto()
    BLUE = enum.auto()
    GREEN = enum.auto()
    RED = enum.auto()
    BLACK = enum.auto()
    GOLD = enum.auto()


class Card:
    """A card including points, gem type, and costs."""
    def __init__(self, points: int, gem_type: Gem, costs: dict[Gem, int]):
        self.points: int = points
        self.gem_type: Gem = gem_type
        self.costs: dict[Gem, int] = costs
    

    def __str__(self) -> str:
        color = ''
        match self.gem_type:
            case Gem.WHITE:
                color = f"{ansi.WHITE}w"
            case Gem.BLUE:
                color = f"{ansi.BLUE}u"
            case Gem.GREEN:
                color = f"{ansi.GREEN}g"
            case Gem.RED:
                color = f"{ansi.RED}r"
            case Gem.BLACK:
                color = f"{ansi.GRAY}k"
        return (f"{ansi.BOLD}{self.points} {color}{ansi.RESET} "
                f"{ansi.WHITE}{self.costs[Gem.WHITE]}"
                f"{ansi.BLUE}{self.costs[Gem.BLUE]}"
                f"{ansi.GREEN}{self.costs[Gem.GREEN]}"
                f"{ansi.RED}{self.costs[Gem.RED]}"
                f"{ansi.GRAY}{self.costs[Gem.BLACK]}"
                f"{ansi.RESET}")
        

class Board:
    """A board with three levels of decks and some number of gems in the center."""
    def __init__(self, filepath: str, shuffle_cards: bool):
        self.gems: dict[Gem, int] = {
            Gem.WHITE: BOARD_GEM_START,
            Gem.BLUE: BOARD_GEM_START,
            Gem.GREEN: BOARD_GEM_START,
            Gem.RED: BOARD_GEM_START,
            Gem.BLACK: BOARD_GEM_START,
            Gem.GOLD: BOARD_GOLD_START
        }
        self.decks: tuple[list[Card], list[Card], list[Card]] = self._load_cards(filepath)
        if shuffle_cards: 
            for deck in self.decks:
                shuffle(deck)
    
    def __array__(self): # TODO!
        pass 

    
    def _load_cards(self, filepath: str) -> tuple[list[Card], list[Card], list[Card]]:
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

        decks = [], [], []
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


class Player:
    """A player that can have purchased cards, reserved cards, and counts for each gem type."""
    def __init__(self):
        self.gems: dict[Gem, int] = {
            Gem.WHITE: PLAYER_GEMS_START,
            Gem.BLUE: PLAYER_GEMS_START,
            Gem.GREEN: PLAYER_GEMS_START,
            Gem.RED: PLAYER_GEMS_START,
            Gem.BLACK: PLAYER_GEMS_START,
            Gem.GOLD: PLAYER_GEMS_START
        }
        self.purchased_cards: list[Card] = []
        self.reserved_cards: list[Card] = []
    
    def _get_points(self):
        return sum(card.points for card in self.purchased_cards)
    
    def __array__(self): # TODO
        pass

class Action(enum.IntEnum):
    RESERVE_00 = enum.auto()
    RESERVE_01 = enum.auto()
    RESERVE_02 = enum.auto()
    RESERVE_03 = enum.auto()
    RESERVE_04 = enum.auto()
    RESERVE_10 = enum.auto()
    RESERVE_11 = enum.auto()
    RESERVE_12 = enum.auto()
    RESERVE_13 = enum.auto()
    RESERVE_14 = enum.auto()
    RESERVE_20 = enum.auto()
    RESERVE_21 = enum.auto()
    RESERVE_22 = enum.auto()
    RESERVE_23 = enum.auto()
    RESERVE_23 = enum.auto()
    RESERVE_24 = enum.auto()
    PURCHASE_00 = enum.auto()
    PURCHASE_01 = enum.auto()
    PURCHASE_02 = enum.auto()
    PURCHASE_03 = enum.auto()
    PURCHASE_10 = enum.auto()
    PURCHASE_11 = enum.auto()
    PURCHASE_12 = enum.auto()
    PURCHASE_13 = enum.auto()
    PURCHASE_20 = enum.auto()
    PURCHASE_21 = enum.auto()
    PURCHASE_22 = enum.auto()
    PURCHASE_23 = enum.auto()
    TAKE3_11100 = enum.auto()
    TAKE3_11010 = enum.auto()
    TAKE3_11001 = enum.auto()
    TAKE3_10110 = enum.auto()
    TAKE3_10101 = enum.auto()
    TAKE3_10011 = enum.auto()
    TAKE3_01110 = enum.auto()
    TAKE3_01101 = enum.auto()
    TAKE3_01011 = enum.auto()
    TAKE3_00111 = enum.auto()
    TAKE2_10000 = enum.auto()
    TAKE2_01000 = enum.auto()
    TAKE2_00100 = enum.auto()
    TAKE2_00010 = enum.auto()
    TAKE2_00001 = enum.auto()
