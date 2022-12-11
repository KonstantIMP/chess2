"""
Base figure's description
"""
from dataclasses import dataclass

from chess2.engine.figure_color import FigureColor
from chess2.engine.figure_type import FigureType
from chess2.engine.position import Position


@dataclass()
class Figure:
    """Base figure's description"""
    type: FigureType
    color: FigureColor
#    position: Position
