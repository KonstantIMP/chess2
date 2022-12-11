"""
Основной класс приложения
"""
from PyQt6.QtWidgets import QApplication
from chess2.utils.bean import BeanManager
import chess2.gui.main_window as mw
import typing as tp


class ChessApplication(QApplication):
    """
    Инициализирует QT и открывает главное окно
    """

    def __init__(self, argv: tp.List[str]) -> None:
        """
        Инициализирует родительсий QApplication,
        основное окно и менеджер элементов (бинов)

        Parameters
        ----------
        argv : tp.List[str], required
            Список входных аргументов приложения (необходимы дя QT)
        """
        super().__init__(argv)

        self.bean_manager = BeanManager()
        self.main_window = mw.ChessMainWindow(self.bean_manager)


    def exec(self):
        """
        Переписывает стандартный exec метод, отображает окно
        игры и начинает обработку событий
        """
        self.main_window.show()
        super().exec()

