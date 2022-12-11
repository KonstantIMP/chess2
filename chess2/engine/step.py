"""
Описание одного игрового шага
"""
from chess2.engine.position import Position
from dataclasses import dataclass
from chess2.engine.event import Event
from chess2.engine.figure import Figure
import typing as tp


@dataclass
class Step:
    """
    Описывает перемещение фигуры из точки a в точку b и события,
    которые это перемещение спровоцировало
    """
    a: Position
    b: Position
    figure: Figure
    events: tp.List[Event]

