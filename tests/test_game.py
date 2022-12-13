"""
Buisness-logic testing
"""
import unittest

from chess2.engine.chess import ChessGame

from chess2.engine.figure_color import FigureColor
from chess2.engine.figure_type import FigureType
from chess2.engine.position import Position
from chess2.engine.figure import Figure

class LogicTest(unittest.TestCase):
    def test_unicode_dump(self):
        game = ChessGame()
        game.create_new_game()

        default_field  = '♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜\n'
        default_field += '♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎\n'
        default_field += (' ' * 15 + '\n') *  4
        default_field += '♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙\n'
        default_field += '♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖'

        self.assertEqual(game.dump_field_to_string(), default_field, msg='Cringe')


    def test_figure_getting(self):
        game = ChessGame()
        game.create_new_game()

        self.assertEqual(game.get_figure('a1'), Figure(FigureType.ROCK, FigureColor.WHITE), msg='Incorrect getting')
        self.assertEqual(game.get_figure((0, 1)), Figure(FigureType.PAWN, FigureColor.BLACK), msg='Incorrect getting')

        with self.assertRaises(Exception):
            game.get_figure((-1, -1))

    
    def test_moves(self):
        game = ChessGame()
        game.create_new_game()

        self.assertNotEqual(game.make_step(Position(0, 6), Position(0, 4)), None)
        self.assertEqual(game.make_step(Position(5, 5), Position(6, 6)), None)

