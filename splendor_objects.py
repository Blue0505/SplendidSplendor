import enum
from random import shuffle
import csv

import ansi_escape_codes as ansi

BOARD_GEM_START: int = 4
BOARD_GOLD_START: int = 5
PLAYER_GEMS_START: int = 0
MAX_RESERVE: int = 3

class Gem(enum.Enum):
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
        self.white_cost = costs[Gem.WHITE]
        self.blue_cost = costs[Gem.BLUE]
        self.green_cost = costs[Gem.GREEN]
        self.red_cost = costs[Gem.RED]
        self.black_cost = costs[Gem.BLACK]
    
    def __repr__(self) -> str:
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
                f"{ansi.WHITE}{self.white_cost}"
                f"{ansi.BLUE}{self.blue_cost}"
                f"{ansi.GREEN}{self.green_cost}"
                f"{ansi.RED}{self.red_cost}"
                f"{ansi.GRAY}{self.black_cost}"
                f"{ansi.RESET}")
        

class Board:
    """A board with three levels of decks and some number of gems in the center."""
    def __init__(self, filepath: str, shuffle_cards: bool):
        self.white_gems = BOARD_GEM_START
        self.blue_gems = BOARD_GEM_START
        self.green_gems = BOARD_GEM_START
        self.red_gems = BOARD_GEM_START
        self.black_gems = BOARD_GEM_START
        self.gold_gems = BOARD_GEM_START
    
        self.decks: list[list[Card]] = self._load_cards(filepath)
        if shuffle_cards: 
            for deck in self.decks:
                shuffle(deck)
    
    def has_gems(self, white=None, blue=None, green=None, red=None, black=None, gold=None) -> bool:
        if white != None and self.white_gems < white:
            return False
        elif blue != None and self.blue_gems < blue:
            return False
        elif green != None and self.green_gems < green:
            return False
        elif red != None and self.red_gems < red:
            return False
        elif black != None and self.black_gems < black:
            return False
        elif gold != None and self.gold_gems < gold:
            return False
        return True
    
    def get_cards(self):
        return [ element for row in self.decks for element in row ] 

    
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

        self._purchased_cards.append(self._reserved_cards[index])
        del self._reserved_cards[index]


    def can_reserve(self) -> bool:
        return len(self._reserved_cards) < MAX_RESERVE
    
    def purchase_card(self, card: Card):
        # TODO: Take gems away and tell board to take card
        self._purchased_cards.append(card)

    def can_purchase(self, card: Card) -> bool:
        if self._white_gems < card.white_cost: return False
        elif self._blue_gems < card.blue_cost: return False
        elif self._green_gems < card.green_cost: return False
        elif self._red_gems < card.red_cost: return False
        elif self._black_gems < card.black_cost: return False
        return True
    
                                                            
    def get_points(self):
        return sum(card.points for card in self._purchased_cards)


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
    PURCHASE_RESERVE_0 = enum.auto()
    PURCHASE_RESERVE_1 = enum.auto()
    PURCHASE_RESERVE_2 = enum.auto()
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
