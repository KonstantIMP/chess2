"""
Available events triggered after step
"""
from dataclasses import dataclass
from enum import Enum

import typing as tp


class EventType(Enum):
    """Available events"""
    KILL    = 0, # Some figure was killed
    UPGRADE = 1, # Pawn at the board end
    WIN     = 2  # King cannot be saved


@dataclass
class Event:
    event_type: EventType
    extra: tp.Any

