import splendor.ansi_escape_codes as ansi
import numpy as np
from numpy.typing import NDArray

from splendor.gem import Gem

class Card:
    """A card including points, gem type, and costs."""
    def __init__(self, points: int, gem_type: Gem, costs: tuple[int,int,int,int,int]):
        self._points: int = points
        self._gem_type: Gem = gem_type
        self._gem_costs: NDArray = np.array(costs)
    
    def get_costs_array(self) -> NDArray:
        return self._gem_costs
    
    def update_gems(self, white=0, blue=0, green=0, red=0, black=0):
        self._gem_costs = self._gem_costs + np.array([white, blue, green, red, black])

    def get_gems_array(self):
        return self._gem_costs

    def __str__(self) -> str:
        color = ''
        match self._gem_type:
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
        return (f"{ansi.BOLD}{self._points} {color}{ansi.RESET} "
                f"{ansi.WHITE}{self._gem_costs[Gem.WHITE]}"
                f"{ansi.BLUE}{self._gem_costs[Gem.BLUE]}"
                f"{ansi.GREEN}{self._gem_costs[Gem.GREEN]}"
                f"{ansi.RED}{self._gem_costs[Gem.RED]}"
                f"{ansi.GRAY}{self._gem_costs[Gem.BLACK]}"
                f"{ansi.RESET}")