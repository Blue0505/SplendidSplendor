import Enum
import 

BOARD_GEM_START: int = 4
BOARD_GOLD_START: int = 5 # TODO: Ensure that this number is correct
PLAYER_GEMS_START: int = 0

class Gem(Enum):
    WHITE = 1
    BLUE = 2
    GREEN = 3
    BLACK = 4
    RED = 5
    GOLD = 6
    

class Card:
    def __init__(self, points: int, gem_type: Gem, costs: dict[Gem, int]):
        self.points = points
        self.gem_type = gem_type
        self.costs = costs
        

class Board:
    def __init__(self, filepath: str):
        self.gems: dict[Gem, int] = {
            Gem.WHITE: BOARD_GEM_START,
            Gem.BLUE: BOARD_GEM_START,
            Gem.GREEN: BOARD_GEM_START,
            Gem.BLACK: BOARD_GEM_START,
            Gem.RED: BOARD_GEM_START,
            Gem.GOLD: BOARD_GOLD_START
        }
        
        self._load_cards(filepath)
    
    def _load_cards(self, filepath: str):
        # TODO: Load cards from JSON. 

class Player:
    def __init__(self):
        self.gems: dict[Gem, int] = {
            Gem.WHITE: PLAYER_GEMS_START,
            Gem.BLUE: PLAYER_GEMS_START,
            Gem.GREEN: PLAYER_GEMS_START,
            Gem.BLACK: PLAYER_GEMS_START,
            Gem.RED: PLAYER_GEMS_START,
            Gem.GOLD: PLAYER_GEMS_START
        }
        self.purchased_cards: list[Card] = []
        self.reserved_cards: list[Card] = []
    
    def _get_points(self):
        return sum(card.points for card in self.purchased_cards)