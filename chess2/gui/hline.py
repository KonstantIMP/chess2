"""
Widget for horizontal line display
"""
from PyQt6.QtWidgets import QFrame


class HLine(QFrame):
    """
    Just a horizontal black line
    """
    def __init__(self):
        super(HLine, self).__init__()

        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

