"""
Wrapper for QT objects
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
import typing as tp

class GuiMapper:
    """
    Converts one QT type to other
    """
    def __init__(self):
        pass


    def box_to_widget(self, box: tp.Union[QVBoxLayout, QHBoxLayout]) -> QWidget:
        """
        Converts vh-box widget to raw QWidget for continuous insertion
        """
        res = QWidget()
        res.setLayout(box)

        return res
