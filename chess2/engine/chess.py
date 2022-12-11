"""
The game's implementation
"""
from chess2.engine.figure_color import FigureColor
from chess2.engine.figure_type import FigureType
from chess2.engine.mapper import FiguresMapper
from chess2.engine.position import Position
from chess2.engine.figure import Figure
from chess2.engine.event import Event, EventType
from chess2.engine.step import Step

from chess2.utils.functions import flatten


import typing as tp


class ChessGame:
    """
    The game's implementation

    Attributes:
    ----------
        field: The game's field and figures on it
        mapper: mapper for figures converting 
        current_color: color of figure's which is available for step
    """
    def __init__(self, mapper: FiguresMapper = FiguresMapper()):
        self.field = self.__generate_empty_field()
        self.mapper = mapper

        self.current_color = FigureColor.WHITE
        self.history: tp.List[Step] = []


    def create_new_game(self) -> None:
        """
        Creates new field with setted figures (in correct order)
        and sets it as a current game's field
        """
        self.field = self.__generate_empty_field()

        for i in range(8):
            self.field[1][i] = Figure(FigureType.PAWN, FigureColor.BLACK)
            self.field[6][i] = Figure(FigureType.PAWN, FigureColor.WHITE)

        for i, el in enumerate([FigureType.ROCK, FigureType.KNIGHT, FigureType.BISHOP]):
            self.field[0][i] = self.field[0][8 - 1 - i] = Figure(el, FigureColor.BLACK)
            self.field[7][i] = self.field[7][8 - 1 - i] = Figure(el, FigureColor.WHITE)

        self.field[7][3] = Figure(FigureType.QUEEN, FigureColor.WHITE)
        self.field[7][4] = Figure(FigureType.KING, FigureColor.WHITE)

        self.field[0][4] = Figure(FigureType.KING, FigureColor.BLACK)
        self.field[0][3] = Figure(FigureType.QUEEN, FigureColor.BLACK)

        self.history = []


    def dump_field_to_string(self) -> str:
        """
        Creates unicode representation of current field

        Returns:
        --------
            string with the field in unicode chars 
        """
        def line_mapper(line: tp.List[Figure]) -> str:
            return ' '.join(
                map(
                    lambda x: ' ' if x is None else self.mapper.map_figure_to_unicode(x),
                    line
                )
            )

        return '\n'.join(
            map(
                line_mapper,
                self.field
            )
        )


    def get_figure(self, position: tp.Union[Position, tp.Tuple[int, int], str]) -> tp.Optional[Figure]:
        """
        Takes figure's coordinates (like indexes or 'LetterDigit' coordinates)
        and returns it (or None if not exsist)
        """
        if not isinstance(position, Position):
            return self.get_figure(self.mapper.map_to_position(position))

        if not position.is_valid():
            raise Exception('Incorrect coordinates were given')

        return self.field[position.y][position.x]


    def get_available_steps(self, position: tp.Union[Position, tp.Tuple[int, int], str]) -> tp.List[Position]:
        """
        Returns available steps for the figure at 'position'
        """
        if not isinstance(position, Position): position = self.mapper.map_to_position(position)

        figure, res = self.get_figure(position), []
        if figure is None: return []

        lines = self.__get_available_line_steps(position)
        diagonals = self.__get_available_diagonal_steps(position)

        match figure.type:
            case FigureType.QUEEN:
                res = flatten(lines + diagonals)
            case FigureType.ROCK:
                res = flatten(lines)
            case FigureType.BISHOP:
                res = flatten(diagonals)
            case FigureType.KING:
                res = flatten(list(map(lambda x: x[0:1], lines + diagonals)))
            case FigureType.KNIGHT:
                res = self.__get_available_knight_steps(position)
            case FigureType.PAWN:
                res = self.__get_available_pawn_steps(position)

        return list(
            filter(
                lambda x: self.get_figure(x) is None or self.get_figure(x).color != self.current_color, res
            )
        )


    def make_step(self, a: Position, b: Position) -> tp.Optional[Step]:
        """
        Moves figure from one point to another if its possible
        """
        if self.get_figure(a).color != self.current_color:
            return None

        if b not in self.get_available_steps(a):
            return None

        events = []

        if self.get_figure(b) is not None:
            events.append(Event(EventType.KILL, self.get_figure(b)))
        if self.get_figure(a).type == FigureType.PAWN and (b.y in [0, 7]):
            events.append(Event(EventType.UPGRADE, None))
            self.field[a.y][a.x] = Figure(FigureType.QUEEN, self.get_figure(a).color)
        if self.get_figure(b) is not None and self.get_figure(b).type == FigureType.KING:
            events.append(Event(EventType.WIN, None))

        self.field[b.y][b.x] = self.field[a.y][a.x]
        self.field[a.y][a.x] = None

        self.__swap_current_color()

        step = Step(a, b, self.get_figure(b), events)
        self.history.append(step)
        return step


    def __get_available_line_steps(self, position: Position) -> tp.List[tp.List[Position]]:
        """
        Returns available steps in horizontal-letf/-right and
        vertical-up/-down directions
        """
        lines = []

        for horizontal_range in [range(position.x + 1, 8), range(position.x - 1, -1, -1)]:
            lines.append([])
            for i in horizontal_range:
                lines[-1].append(Position(i, position.y))
                if self.get_figure(lines[-1][-1]) is not None:
                    break

        for vertical_range in [range(position.y + 1, 8), range(position.y - 1, -1, -1)]:
            lines.append([])
            for i in vertical_range:
                lines[-1].append(Position(position.x, i))
                if self.get_figure(lines[-1][-1]) is not None:
                    break

        return lines

    
    def __get_available_diagonal_steps(self, position: Position) -> tp.List[tp.List[Position]]:
        """
        Returns available steps in diagonal directions
        """
        diagonals = []

        diagonal_directions = [
            (range(1, min(7 - position.x, 7 - position.y) + 1), (1, 1)),
            (range(1, min(7 - position.x, position.y) + 1), (1, -1)),
            (range(1, min(position.x, 7 - position.y) + 1), (-1, 1)),
            (range(1, min(position.x, position.y) + 1), (-1, -1))
        ]

        for direction in diagonal_directions:
            diagonals.append([])
            x_mul, y_mul = direction[1]
            for inc in direction[0]:
                diagonals[-1].append(Position(position.x + inc * x_mul, position.y + inc * y_mul))
                if self.get_figure(diagonals[-1][-1]) is not None:
                    break

        return diagonals


    def __get_available_knight_steps(self, position: Position) -> tp.List[Position]:
        """
        Get available steps for knight figure
        """
        res = []

        for step_type in [(1, 2), (2, 1)]:
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                res.append(Position(position.x + step_type[0] * direction[0], position.y + step_type[1] * direction[1]))
        
        return list(filter(lambda x: x.is_valid(), res))


    def __get_available_pawn_steps(self, position: Position) -> tp.List[Position]:
        """
        Get available steps for pawn figure
        """
        direction_mul = 1 if self.get_figure(position).color == FigureColor.BLACK else -1

        res = [Position(position.x, position.y + direction_mul)]
        if self.get_figure(res[0]) is None:
            if (direction_mul == 1 and position.y == 1) or (direction_mul == -1 and position.y == 6):
                if self.get_figure(Position(position.x, position.y + direction_mul)) is None:
                    res.append(Position(position.x, position.y + 2 * direction_mul))
        else: res = []

        temp = [
            Position(position.x - 1, position.y + direction_mul),
            Position(position.x + 1, position.y + direction_mul)
        ]

        for p in temp:
            if p.is_valid() and self.get_figure(p) is not None:
                res.append(p)

        return list(filter(lambda x: x.is_valid(), res))


    def get_figures(self, filter_color: tp.Optional[FigureColor] = None) -> tp.List[tp.Tuple[Figure, Position]]:
        """
        Returns figures and it's positions 

        Parameters:
        ----------
        filter_color: tp.Optional[FigureColor], optional
            Filters the output by color 
        """
        res = []

        for i in range(8):
            for j in range(8):
                temp = self.field[i][j]
                if temp is not None:
                    res.append((temp, Position(j, i)))

        if filter_color is not None:
            res = list(
                filter(
                    lambda x: x[0].color == filter_color,
                    res
                )
            )

        return res


    def __swap_current_color(self) -> None:
        """
        Changes current color (next player)
        """
        self.current_color = FigureColor.BLACK if self.current_color == FigureColor.WHITE else FigureColor.WHITE


    def __generate_empty_field(self) -> tp.List[tp.List[tp.Optional[Figure]]]:
        """
        Creates an empty chess field (no any figures)

        Returns:
            Array of chess field's rows
        """
        return [[None for _ in range(8)] for __ in range(8)]

