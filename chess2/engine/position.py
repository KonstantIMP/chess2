"""
Class for representing figure's position
"""
from dataclasses import dataclass


@dataclass()
class Position:
    """
    Class for representing figure's position
    x - index of column, y - index of row (top to bottom order)
    """
    x: int
    y: int

    def is_valid(self) -> bool:
        """
        Checks is the given position correct
        """
        return 0 <= self.x <= 7 and 0 <= self.y <= 7
