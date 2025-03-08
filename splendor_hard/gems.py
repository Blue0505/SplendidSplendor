import numpy as np
from numpy.typing import NDArray
import splendor_hard.ansi_escape_codes as ansi

class Gems:
    """A gem container for the board, players, and cards."""

    def __init__(self, gems: NDArray):
        self._gems = gems
    
    def get_array(self):
        return self._gems

    def has_at_least(self, gems: NDArray) -> bool:
       return not np.any(self._gems < gems)

    def update(self, gems: NDArray) -> NDArray: 
        self._gems = self._gems + gems

    def get_gold(self) -> int:
        return self._gems[5]

    def has_gold(self) -> int:
        return self._gems[5] > 0
    
    def get_gem_sum(self) -> int:
        return np.sum(self._gems)

def gem_array_str(gem_array, gold=False) -> str:
    """Returns a string representation of a gem array and (optionally) gold."""
    output = (
        f"{ansi.WHITE}{gem_array[0]} {ansi.BLUE}{gem_array[1]} "
        f"{ansi.GREEN}{gem_array[2]} {ansi.RED}{gem_array[3]} "
        f"{ansi.GRAY}{gem_array[4]}{ansi.RESET}"
    )

    if gold is not False:
        output += f" {ansi.YELLOW}{gem_array[5]}{ansi.RESET}"
    return output