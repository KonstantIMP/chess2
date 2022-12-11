"""
Base application class for the Chess 2.0
"""
from PyQt6.QtWidgets import QApplication
from chess2.utils.bean import BeanManager
import chess2.gui.main_window as mw
import typing as tp


class ChessApplication(QApplication):
    """
    Inits the Qt framework and open main window
    """

    def __init__(self, argv: tp.List[str]) -> None:
        """
        Inits the base QApplication instance

        Parameters
        ----------
        argv : tp.List[str], required
            Input command line for the app (need for the Qt debug)
        """
        super().__init__(argv)

        self.bean_manager = BeanManager()
        self.main_window = mw.ChessMainWindow(self.bean_manager)


    def exec(self):
        """
        Overrides default exec method, shows the main window
        and starts events looping
        """
        self.main_window.show()
        super().exec()

