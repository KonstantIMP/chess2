"""
Main app's window
"""
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QListView, QSizePolicy
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QAbstractItemView
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtCore import QStringListModel

from chess2.gui.board import ChessBoard
from chess2.gui.aspect_ratio_widget import AspectRatioWidget
from chess2.gui.hline import HLine
from chess2.engine.step import Step
from chess2.engine.event import EventType
from chess2.utils.bean import BeanManager

import typing as tp


class ChessMainWindow(QMainWindow):
    """
    Contains all base elements, displays the play field
    """

    def __init__(self, bmg: BeanManager) -> None:
        super().__init__()

        self.figures_mapper = bmg.figures_mapper
        self.gui_mapper = bmg.gui_mapper
        self.helper = bmg.helper
        self.engine = bmg.engine
        self.cfg = bmg.config

        self.list_model = QStringListModel()

        self.__create_ui()


    def __create_ui(self) -> None:
        """
        Creates children, sets styles and titles
        """
        self.setWindowTitle('Chess 2.0')
        self.resize(800, 450)

        history_panel = self.__create_history_panel()
        game_panel = self.__create_game_board()
        control_panel = self.__create_control_panel()

        layout = QHBoxLayout()
        layout.addWidget(history_panel, 3)
        layout.addWidget(game_panel, 7)
        layout.addWidget(control_panel, 2)

        container = QWidget()
        container.setLayout(layout)

        super().setCentralWidget(container)


    def __create_history_panel(self) -> QWidget:
        """
        Creates panel with scrollable list of steps
        """
        box = QVBoxLayout()
        box.addWidget(QLabel('History'))

        list_view = QListView()
        list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        list_view.setModel(self.list_model)
        list_view.setMinimumWidth(176)

        list_view.setStyleSheet('QListView { font-size: 16px; }')
        box.addWidget(list_view)

        return self.gui_mapper.box_to_widget(box)


    def __create_game_board(self) -> QWidget:
        """
        Creates 8x8 grid with figures and empty cells
        """
        self.board = ChessBoard(self.cfg, self.engine, self.figures_mapper)
        self.board.onStep.connect(self.__on_step_done)
        self.board.setEnabled(False)
        return AspectRatioWidget(self.board)


    def __on_step_done(self, step: Step) -> None:
        from chess2.engine.figure_color import FigureColor as FC

        events = []
        for e in step.events:
            if e.event_type == EventType.UPGRADE: events.append(f'U')
            if e.event_type == EventType.KILL:
                events.append(f'K{self.figures_mapper.map_figure_to_unicode(e.extra)}')
            if e.event_type == EventType.WIN:
                self.__show_message_dialog(f"""Wow! Somebody won: {
                    'WHITE' if self.engine.current_color == FC.BLACK else 'BLACK'
                }""")
                self.board.setEnabled(False)

        res = f"""{
                self.figures_mapper.map_figure_to_unicode(step.figure)
            }: {
                self.figures_mapper.map_position(step.a)
            } ⟶ {
                self.figures_mapper.map_position(step.b)
            } {(' : ' + ' '.join(events)) if len(events) != 0 else ''}
        """

        self.list_model.insertRows(0, 1)
        index = self.list_model.index(0)

        self.list_model.setData(index, res)
        self.__update_current_color()

        print(res)

    def __create_control_panel(self) -> QWidget:
        """
        Panel with buttons like 'save', 'load', 'new'
        """
        from PyQt6.QtWidgets import QSpacerItem

        box = QVBoxLayout()

        new_game = QPushButton('New game')
        new_game.clicked.connect(self.__create_new_game)
        box.addWidget(new_game)
        box.addWidget(HLine())

        load_btn = QPushButton('Load game')
        load_btn.clicked.connect(self.__load_game)
        box.addWidget(load_btn)

        save_btn = QPushButton('Save game')
        save_btn.clicked.connect(self.__save_game)
        box.addWidget(save_btn)
        box.addWidget(HLine())

        delete_btn = QPushButton('Delete game')
        delete_btn.clicked.connect(self.__delete_saved_game)
        box.addWidget(delete_btn)

        box.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Policy.Expanding))
        box.addWidget(self.__create_step_info_block())
        box.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Policy.Expanding))

        exit_btn = QPushButton('Exit')
        exit_btn.clicked.connect(lambda x: self.close())
        box.addWidget(exit_btn)

        return self.gui_mapper.box_to_widget(box)


    def __create_step_info_block(self) -> QWidget:
        box = QVBoxLayout()

        cc = QHBoxLayout()

        msg = QLabel('Current color is')
        msg.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))

        self.color_state = QPushButton('')
        self.color_state.setMaximumSize(24, 24)

        cc.addWidget(msg)
        cc.addWidget(self.color_state)

        box.addWidget(self.gui_mapper.box_to_widget(cc))

        give_up_btn = QPushButton('Give up')
        give_up_btn.clicked.connect(self.__give_up)
        box.addWidget(give_up_btn)

        box.setContentsMargins(0, 0, 0, 0)
        return self.gui_mapper.box_to_widget(box)


    def __update_current_color(self) -> None:
        from chess2.engine.figure_color import FigureColor
        self.color_state.setStyleSheet(f"""
            QPushButton {{ background-color: {
                self.cfg['non_oven_cell_color'] if self.engine.current_color == FigureColor.BLACK else self.cfg['oven_cell_color']
            };}}
        """
        )

    def __create_new_game(self) -> None:
        self.engine.create_new_game()
        self.board.update_field()
        self.__clear_history_panel()
        self.__update_current_color()
        self.board.setEnabled(True)


    def __give_up(self):
        self.board.setEnabled(False)
        self.__show_message_dialog(f'{str(self.engine.current_color).split(".")[-1]} has gave up')

    def __save_game(self) -> None:
        if not self.board.isEnabled():
            self.__show_message_dialog('Nothing to save')
            return

        text, ok = QInputDialog.getText(self, 'Game saving', 'Enter the game`s name')

        if ok:
            try:
                if text in self.helper.get_saved_games():
                    self.__show_message_dialog(f'Give with the "{text}" name already exists')
                    return

                self.helper.save_game(self.engine, text)
                self.__show_message_dialog('Game saved')
            except Exception:
                self.__show_message_dialog('Something went wrong')


    def __load_game(self) -> None:
        games = self.helper.get_saved_games()
        text, ok = QInputDialog.getItem(self, 'Game loading', 'Select game for load', games, 0, False)

        if ok:
            try:
                self.helper.load_game(text, self.engine)
                self.board.update_field()
                self.__clear_history_panel()

                for step in self.engine.history:
                    self.__on_step_done(step)
                self.board.setEnabled(True)

                self.__show_message_dialog('Game loaded')
            except Exception:
                self.__show_message_dialog('Something went wrong')

    def __clear_history_panel(self) -> None:
        self.list_model.removeRows(0, self.list_model.rowCount())


    def __delete_saved_game(self) -> None:
        """Deletes saved game from db"""
        games = self.helper.get_saved_games()
        text, ok = QInputDialog.getItem(self, 'Game deletion', 'Select game for remove', games, 0, False)

        if ok:
            try:
                self.helper.delete_game(text)
                self.__show_message_dialog('Game was deleted')
            except Exception:
                self.__show_message_dialog('Cant remove the game')

    def __show_message_dialog(self, msg: str) -> None:
        from PyQt6.QtWidgets import QMessageBox

        box = QMessageBox(self)
        box.setWindowTitle('Important message')
        box.setMinimumWidth(300)
        box.setText(msg)

        box.show()
