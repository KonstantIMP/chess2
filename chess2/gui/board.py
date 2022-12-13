"""
Виджет для отображения игровой доски
"""
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from chess2.engine.chess import ChessGame
from chess2.engine.mapper import FiguresMapper
from chess2.engine.step import Step
from chess2.engine.position import Position

import typing as tp

class ChessBoard(QWidget):
    onStep = pyqtSignal(Step, name='onStep')

    """
    Отображение сетки кнопок 8 на 8
    """
    def __init__(self, config: tp.Dict, engine: ChessGame, mapper: FiguresMapper):
        super(ChessBoard, self).__init__()

        self.mapper = mapper
        self.engine = engine
        self.cfg = config

        self.buttons = self.__generate_buttons()
        self.grid = self.__create_root_grid()

        self.setLayout(self.grid)
        self.update_field()

        self.non_base = []


    def update_field(self):
        """Устанавливает на кнопки с фигурами картинки"""
        for row in self.buttons:
            for btn in row:
                btn.setIcon(QIcon())

        for figure in self.engine.get_figures():
            icon = QIcon(self.mapper.map_figure_to_svg(figure[0]))
            self.buttons[figure[1].y][figure[1].x].setIcon(icon)


    def __clear_to_base(self):
        """
        Убирает нестандартные стили с кнопок
        """
        for pos in self.non_base:
            self.buttons[pos.y][pos.x].setStyleSheet(self.__generate_base_style(pos))

        self.non_base = []

    def __create_root_grid(self) -> QGridLayout:
        """
        Заполняет сетку ранее созданными кнопками
        """
        grid = QGridLayout()

        for i in range(8):
            for j in range(8):
                grid.addWidget(self.buttons[i][j], i, j, 1, 1)

        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(3)
        grid.setVerticalSpacing(3)

        return grid

    def __generate_buttons(self) -> tp.List[tp.List[QPushButton]]:
        """
        Создает матрицу из кнопок (с необходимыми стилями)
        """
        from functools import partial

        res = []

        for i in range(8):
            res.append([])
            for j in range(8):
                btn = QPushButton('')

                btn.setMinimumSize(self.cfg['min_figure_size'], self.cfg['min_figure_size'])
                btn.setStyleSheet(self.__generate_base_style(Position(x=i, y=j)))
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                btn.setIconSize(QSize(40, 40))

                btn.pressed.connect(partial(self.__chess_button_pressed, Position(x=j, y=i)))

                res[-1].append(btn)

        return res


    def __generate_base_style(self, position: Position) -> str:
        """
        Генерирует стиль для базовых яччек (туда нет хода, там нет фигуры и тп).
        """
        return f"""
            QPushButton {{
                background-color: {
                    self.cfg['oven_cell_color'] if (position.x + position.y) % 2 == 0 else self.cfg['non_oven_cell_color']
                };
                border: 0px solid black;
            }}
            QPushButton:hover
            {{
                background-color: {
                    self.cfg['hover_color']
                };
                border: 0px solid black;
            }}
            QPushButton:pressed {{
                background-color: {
                    self.cfg['pressed_color']
                };
            }}
        """


    def __generate_danger_style(self) -> str:
        """
        Стиль для клеток, на которых находится фигура в опасности
        """
        return f"""
            QPushButton {{
                background-color: {
                    self.cfg['danger_color']
                };
                border: 0px solid black;
            }}
            QPushButton:hover
            {{
                background-color: {
                    self.cfg['danger_hover_color']
                };
                border: 0px solid black;
            }}
        """

    def __generate_step_style(self) -> str:
        """
        Стиль для клеток, куда можно выполнить ход
        """
        return f"""
            QPushButton {{
                background-color: {
                    self.cfg['step_color']
                };
                border: 0px solid black;
            }}
            QPushButton:hover {{
                background-color: {
                    self.cfg['step_hover_color']
                };
                border: 0px solid black;
            }}
        """
        

    
    def __generate_castling_style(self) -> str:
        """
        Стиль для клеток, с возможной рокировкой
        """
        return f"""
            QPushButton {{
                background-color: {
                    self.cfg['castling_color']
                };
                border: 0px solid black;
            }}
            QPushButton:hover {{
                background-color: {
                    self.cfg['castling_hover_color']
                };
                border: 0px solid black;
            }}
        """


    def __chess_button_pressed(self, position: Position) -> None:
        """
        Событие при нажатии на одну из кнопок
        """
        if position in self.non_base:
            self.__process_step(position)
            return
        self.__clear_to_base()

        current_figure = self.engine.get_figure(position)
        if current_figure is None or current_figure.color != self.engine.current_color:
            return

        self.buttons[position.y][position.x].setStyleSheet(
            f"QPushButton {{background-color: {self.cfg['current_color']};}}"
        )
        self.non_base.append(position)

        available_steps = self.engine.get_available_steps(position)
        for pos in available_steps:
            self.buttons[pos.y][pos.x].setStyleSheet(
                self.__generate_step_style() if self.engine.get_figure(pos) is None else 
                (self.__generate_danger_style() if current_figure.color != self.engine.get_figure(pos).color else self.__generate_castling_style())
            )
            self.non_base.append(pos)


    def __process_step(self, position: Position) -> None:
        """Выполняет ход из позиции в позицию"""
        step = self.engine.make_step(self.non_base[0], position)
        if step is None: return

        self.update_field()

        self.__clear_to_base()
        self.onStep.emit(step)

