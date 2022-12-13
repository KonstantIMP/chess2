"""
Основная логика игры
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
    Логика игры

    Атрибуты:
    ----------
        field: 8 на 8 поле с фигурами
        mapper: конвертер для фигур и их расположений 
        current_color: цвет игрока, чей ход сейчас
        king_moves: перемещался ли король
    """
    def __init__(self, mapper: FiguresMapper = FiguresMapper()):
        self.field = self.__generate_empty_field()
        self.mapper = mapper

        self.current_color = FigureColor.WHITE
        self.history: tp.List[Step] = []

        self.king_moves = dict()


    def create_new_game(self) -> None:
        """
        Создает новое поле и заполняет его начальными значениями
        """
        self.field = self.__generate_empty_field()
        self.current_color = FigureColor.WHITE

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

        self.king_moves[FigureColor.BLACK] = False
        self.king_moves[FigureColor.WHITE] = False

        self.history = []


    def dump_field_to_string(self) -> str:
        """
        Переводит поле в строку из unicode символов
        (для тестов и отображения через консоль)
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
        Возвращает фигуру, расположенную на указанной позиции
        Если на позиции нет фигуры, возвращает None
        """
        if not isinstance(position, Position):
            return self.get_figure(self.mapper.map_to_position(position))

        if not position.is_valid():
            raise Exception('Incorrect coordinates were given')

        return self.field[position.y][position.x]


    def get_available_steps(self, position: tp.Union[Position, tp.Tuple[int, int], str], check_castling: bool = True) -> tp.List[Position]:
        """
        Возвращает возможные позиции, куда может совершить ход
        фигура, по заданным координатам
        """
        if not isinstance(position, Position): position = self.mapper.map_to_position(position)

        figure, res, extra = self.get_figure(position), [], []
        if figure is None: return []

        lines = self.__get_available_line_steps(position)
        diagonals = self.__get_available_diagonal_steps(position)

        match figure.type:
            case FigureType.QUEEN:
                res = flatten(lines + diagonals)
            case FigureType.ROCK:
                res = flatten(lines)
                if check_castling:
                    castling = self.__check_rock_castling(position)
                    if castling is not None: extra.append(castling)
            case FigureType.BISHOP:
                res = flatten(diagonals)
            case FigureType.KING:
                res = flatten(list(map(lambda x: x[0:1], lines + diagonals)))
                if check_castling:
                    castling = self.__check_king_castling(position)
                    if castling is not None: extra.append(castling)
            case FigureType.KNIGHT:
                res = self.__get_available_knight_steps(position)
            case FigureType.PAWN:
                res = self.__get_available_pawn_steps(position)

        return list(
            filter(
                lambda x: self.get_figure(x) is None or self.get_figure(x).color != self.current_color, res
            )
        ) + extra


    def make_step(self, a: Position, b: Position) -> tp.Optional[Step]:
        """
        Выполняет ход фигуры из a в b
        Если ход невозможен, возвращает None
        """
        if self.get_figure(a) is None or self.get_figure(a).color != self.current_color or b not in self.get_available_steps(a):
            return None

        events, castling = [], self.get_figure(b) is not None and self.get_figure(a).color == self.get_figure(b).color

        if self.get_figure(b) is not None and self.get_figure(a).color != self.get_figure(b).color:
            events.append(Event(EventType.KILL, self.get_figure(b)))
        if self.get_figure(a).type == FigureType.PAWN and (b.y in [0, 7]):
            events.append(Event(EventType.UPGRADE, None))
            self.field[a.y][a.x] = Figure(FigureType.QUEEN, self.get_figure(a).color)
        if self.get_figure(b) is not None and self.get_figure(b).type == FigureType.KING:
            if self.get_figure(a).color != self.get_figure(b).color:
                events.append(Event(EventType.WIN, None))

        if castling == True:
            self.king_moves[self.get_figure(a).color] = True
            king, kp, rock, rp = self.get_figure(a), a, self.get_figure(b), b
            if king.type != FigureType.KING: king, kp, rock, rp = rock, rp, king, kp
            direction_mul = 1 if rp.x == 7 else -1

            self.field[kp.y][kp.x + direction_mul], self.field[rp.y][rp.x], self.field[kp.y][kp.x] = rock, None, None
            self.field[kp.y][kp.x + 2 * direction_mul] = king

            b = Position(kp.x + 2 * direction_mul, kp.y)
            events.append(Event(EventType.CASTLING, None))
        else:
            if self.get_figure(a).type == FigureType.KING:
                self.king_moves[self.get_figure(a).color] = True
            self.field[b.y][b.x] = self.field[a.y][a.x]
            self.field[a.y][a.x] = None

        self.__swap_current_color()
        self.history.append(Step(a, b, self.get_figure(b), events))
        return self.history[-1]


    def __get_available_line_steps(self, position: Position) -> tp.List[tp.List[Position]]:
        """
        Возвращает все свободные клетки по горизонтали и вертикали
        от заданной позиции
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


    def __check_rock_castling(self, position: Position) -> tp.Optional[Position]:
        """
        Проверяет, возможно ли выполнить рокировку ладьей
        Если да, то возвращает координаты короля
        """
        rock = self.get_figure(position)
        if rock is None or rock.type != FigureType.ROCK or self.king_moves[rock.color] or position.x not in [0, 7]:
            return None

        king_pos = Position(x=4, y=0 if rock.color == FigureColor.BLACK else 7)
        if king_pos.y != position.y:
            return None
        
        for i in range(min(position.x, king_pos.x) + 1, max(position.x, king_pos.x)):
            temp_pos = Position(x=i, y=position.y)
            if self.get_figure(temp_pos) is not None:
                return None
            if self.__is_position_in_dager(temp_pos, FigureColor.BLACK if rock.color == FigureColor.WHITE else FigureColor.WHITE):
                return None

        return king_pos


    def __check_king_castling(self, position: Position) -> tp.Optional[Position]:
        """
        Проверяет, позможно ли выполнить рокировку королем
        Если да, то возвращает координаты ладьи
        """
        king = self.get_figure(position)
        if king is None or king.type != FigureType.KING or self.king_moves[king.color]:
            return None

        for rock in filter(lambda x: x[0].type == FigureType.ROCK, self.get_figures(king.color)):
            temp = self.__check_rock_castling(rock[1])
            if temp is not None: return rock[1]

        return None

    
    def __get_available_diagonal_steps(self, position: Position) -> tp.List[tp.List[Position]]:
        """
        Возвращает все свободные клетки по диагоналям от заданной позиции
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
        Доступные перемещения для коня
        """
        res = []

        for step_type in [(1, 2), (2, 1)]:
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                res.append(Position(position.x + step_type[0] * direction[0], position.y + step_type[1] * direction[1]))
        
        return list(filter(lambda x: x.is_valid(), res))


    def __get_available_pawn_steps(self, position: Position) -> tp.List[Position]:
        """
        Доступные перемещения для пешки
        """
        direction_mul = 1 if self.get_figure(position).color == FigureColor.BLACK else -1

        res = [Position(position.x, position.y + direction_mul)]
        if self.get_figure(res[0]) is None:
            if (direction_mul == 1 and position.y == 1) or (direction_mul == -1 and position.y == 6):
                if self.get_figure(Position(position.x, position.y + direction_mul)) is None:
                    res.append(Position(position.x, position.y + 2 * direction_mul))
                    if self.get_figure(res[-1]) is not None: res = res[:len(res) - 1]
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
        Возвращает список всех фигур и их расположений на доске

        Параметры:
        ----------
        filter_color: tp.Optional[FigureColor], optional
            Фильтрует фигуры по цвету (можно получить только
            фигуры определенного цвета) 
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


    def __is_position_in_dager(self, position: Position, danger_from: tp.Optional[FigureColor] = None) -> bool:
        """
        Проверяет, находится ли заданная клетка в опсаности
        """
        all_steps = list()

        temp_figure = self.get_figure(position)
        if temp_figure is not None:
            for enemy in self.get_figures(FigureColor.WHITE if temp_figure.color == FigureColor.BLACK else FigureColor.BLACK):
                all_steps += self.get_available_steps(enemy[1], False)
        elif danger_from is not None:
            for enemy in self.get_figures(danger_from):
                all_steps += self.get_available_steps(enemy[1], False)
        else:
            for enemy in self.get_figures():
                all_steps += self.get_available_steps(enemy[1], False)

        return position in all_steps


    def __swap_current_color(self) -> None:
        """
        Переход к ходу следующего игрока
        """
        self.current_color = FigureColor.BLACK if self.current_color == FigureColor.WHITE else FigureColor.WHITE


    def __generate_empty_field(self) -> tp.List[tp.List[tp.Optional[Figure]]]:
        """
        Создает полностью пустое поле, заполненное None
        """
        return [[None for _ in range(8)] for __ in range(8)]

