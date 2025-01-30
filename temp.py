from enum import Enum
from random import shuffle
import csv

import ansi_escape_codes as ansi

BOARD_GEM_START: int = 4    # 2 player games start with 4 gems of each type
BOARD_GOLD_START: int = 5   # All games start with 5 gold
PLAYER_GEMS_START: int = 0

class Gem(Enum):
    WHITE = 1
    BLUE = 2
    GREEN = 3
    RED = 4
    BLACK = 5
    GOLD = 6


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
    def __init__(self, filepath: str):
        self.gems: dict[Gem, int] = {
            Gem.WHITE: BOARD_GEM_START,
            Gem.BLUE: BOARD_GEM_START,
            Gem.GREEN: BOARD_GEM_START,
            Gem.RED: BOARD_GEM_START,
            Gem.BLACK: BOARD_GEM_START,
            Gem.GOLD: BOARD_GOLD_START
        }
        self.decks: tuple[list[Card], list[Card], list[Card]] = self._load_cards(filepath)
        for deck in self.decks:
            shuffle(deck)

    
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
            csvreader = csv.DictReader(csvfile, restval='0')
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
