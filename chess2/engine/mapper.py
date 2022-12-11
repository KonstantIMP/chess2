"""
Mapping from Figure class to displayable values
"""
from chess2.engine.figure import Figure
from chess2.engine.position import Position
from chess2.engine.figure_color import FigureColor

from pkg_resources import resource_filename
import typing as tp


class FiguresMapper:
    """
    Class for mapping Figure class to displayable value
    and Positions converting

    Attributes:
    ----------
        image_mapping - links to the images for figures display
    """
    def __init__(self):
        self.image_mapping = dict()


    def map_figure_to_unicode(self, figure: Figure) -> str:
        """
        Maps figure to unicode character for display
        """
        return figure.type.value[figure.color.value]


    def map_figure_to_svg(self, figure: Figure) -> str:
        """
        Returns path to the svg with the figure's image
        """
        return resource_filename(
            'chess_2_0.resources',
            ('b' if figure.color == FigureColor.BLACK else 'w') + '_' + str(figure.type).lower().split('.')[-1] + '.svg'
        )


    def map_to_position(self, position: tp.Union[tp.Tuple[int, int], str]) -> Position:
        """
        Converts figure's coordinates to Position struct
        """
        if isinstance(position, str):
            coordinates = (ord(position.lower()[0]) - ord('a'), ord('8') - ord(position[1]))
            return Position(coordinates[0], coordinates[1])
        elif isinstance(position, tuple):
            return Position(position[0], position[1])
        raise Exception('Unavailable position format')


    def map_position(self, position: Position) -> str:
        """
        Converts Position to human readable format
        """
        return f'{chr(ord("A") + position.x)}{8 - position.y}'

