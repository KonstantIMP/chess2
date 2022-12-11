"""
Description of step
"""
from chess2.engine.position import Position
from dataclasses import dataclass
from chess2.engine.event import Event
from chess2.engine.figure import Figure
import typing as tp


@dataclass
class Step:
    """
    describes figure's move from point a to point b
    """
    a: Position
    b: Position
    figure: Figure
    events: tp.List[Event]

