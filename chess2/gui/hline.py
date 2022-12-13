"""
Горизонтальная линия(отделитель)
Виджет, элемент интерфейса
"""
from PyQt6.QtWidgets import QFrame


class HLine(QFrame):
    """
    Черная горизонтальная полоса
    QFrame модифицируем в линию
    """
    def __init__(self):
        super(HLine, self).__init__()
        """
            последние две строки
делают из квадрата
горизонтальную линию
            """
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

