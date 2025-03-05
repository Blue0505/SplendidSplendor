import numpy as np
from numpy.typing import NDArray

from splendor.gem import Gem
import splendor.ansi_escape_codes as ansi
from splendor.gems import Gems


class Card:
    """A card including points, gem type, and costs."""

    def __init__(
        self, points: int, gem_type: Gem, costs: tuple[int, int, int, int, int]
    ):
        self.points: int = points
        self.gem_type: Gem = gem_type
        self.gems = Gems([*np.array(costs), 0])

    def __array__(self) -> NDArray:
        return np.array([
            self.points,
            self.gem_type == Gem.WHITE,
            self.gem_type == Gem.BLUE,
            self.gem_type == Gem.GREEN,
            self.gem_type == Gem.RED,
            self.gem_type == Gem.BLACK,
            *(self.gems.get_array()[:5])
        ])

    def __str__(self) -> str:
        color = ""
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
        return (
            f"{ansi.BOLD}{self.points} {color}{ansi.RESET} "
            f"{ansi.WHITE}{self.gems.get_array()[Gem.WHITE]}"
            f"{ansi.BLUE}{self.gems.get_array()[Gem.BLUE]}"
            f"{ansi.GREEN}{self.gems.get_array()[Gem.GREEN]}"
            f"{ansi.RED}{self.gems.get_array()[Gem.RED]}"
            f"{ansi.GRAY}{self.gems.get_array()[Gem.BLACK]}"
            f"{ansi.RESET}"
        )

    
