"""
Описание фигуры
"""
from dataclasses import dataclass

from chess2.engine.figure_color import FigureColor
from chess2.engine.figure_type import FigureType
from chess2.engine.position import Position


@dataclass()
class Figure:
    """Каждая фигура состоит из типа и цвета"""
    type: FigureType
    color: FigureColor
#    position: Position
