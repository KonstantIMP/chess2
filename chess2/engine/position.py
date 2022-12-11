"""
Описание положения фигуры на доске
"""
from dataclasses import dataclass


@dataclass()
class Position:
    """
    Описание положожения фигуры на игрвом поле
    x - индекс колонки, y - индекс столбца
    """
    x: int
    y: int

    def is_valid(self) -> bool:
        """
        Проверяет текующую позицию на корректность
        """
        return 0 <= self.x <= 7 and 0 <= self.y <= 7
