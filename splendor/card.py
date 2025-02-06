from .gem import Gem
import ansi_escape_codes as ansi

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