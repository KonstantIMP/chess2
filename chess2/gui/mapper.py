"""
Конвертер QT типов
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
import typing as tp

class GuiMapper:
    def __init__(self):
        pass


    def box_to_widget(self, box: tp.Union[QVBoxLayout, QHBoxLayout]) -> QWidget:
        """
        Переводит контейнер в виджет
        """
        res = QWidget()
        res.setLayout(box)

        return res
