"""
Возможные виды событий
"""
from dataclasses import dataclass
from enum import Enum

import typing as tp


class EventType(Enum):
    """Доступные события"""
    KILL    = 0, # Убийство фигуры
    UPGRADE = 1, # Пешка проапгрейдилась
    WIN     = 2  # Короля убили


@dataclass
class Event:
    event_type: EventType
    extra: tp.Any

