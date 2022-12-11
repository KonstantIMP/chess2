"""
Транслирует оюъект Figure в изображение или в путь до картинки
"""
from chess2.engine.figure import Figure
from chess2.engine.position import Position
from chess2.engine.figure_color import FigureColor

from pkg_resources import resource_filename
import typing as tp


class FiguresMapper:
    """
    переводит обхект Figure в отображаемый формат
    """
    def __init__(self):
        pass


    def map_figure_to_unicode(self, figure: Figure) -> str:
        """
        Переводит фигуру в символ юникода
        """
        return figure.type.value[figure.color.value]


    def map_figure_to_svg(self, figure: Figure) -> str:
        """
        Возвращает путь до картинки с изображением фигуры
        """
        return resource_filename(
            'chess2.resources',
            ('b' if figure.color == FigureColor.BLACK else 'w') + '_' + str(figure.type).lower().split('.')[-1] + '.svg'
        )


    def map_to_position(self, position: tp.Union[tp.Tuple[int, int], str]) -> Position:
        """
        Переводит любой формат координат в Position
        """
        if isinstance(position, str):
            coordinates = (ord(position.lower()[0]) - ord('a'), ord('8') - ord(position[1]))
            return Position(coordinates[0], coordinates[1])
        elif isinstance(position, tuple):
            return Position(position[0], position[1])
        raise Exception('Unavailable position format')


    def map_position(self, position: Position) -> str:
        """
        Переводит Position в шахматный формат (буквацифра)
        """
        return f'{chr(ord("A") + position.x)}{8 - position.y}'

