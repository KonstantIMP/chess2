"""
Горизонтальная линия(отделитель)
"""
from PyQt6.QtWidgets import QFrame


class HLine(QFrame):
    """
    Черная горизонтальная полоса
    """
    def __init__(self):
        super(HLine, self).__init__()

        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

