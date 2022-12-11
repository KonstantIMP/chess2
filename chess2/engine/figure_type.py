"""
Supported figure types
"""
from enum import Enum


class FigureType(Enum):
    """Supported figure types"""
    PAWN   = ('♙', '♟︎') # пешка
    ROCK   = ('♖', '♜') # Башня
    KNIGHT = ('♘', '♞') # Конь
    BISHOP = ('♗', '♝') # Офицер
    QUEEN  = ('♕', '♛') # Королева
    KING   = ('♔', '♚') # Король
