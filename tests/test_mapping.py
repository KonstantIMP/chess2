"""
Mapping testing
"""
import unittest

from chess2.engine.mapper import FiguresMapper
from chess2.engine.figure_color import FigureColor
from chess2.engine.figure_type import FigureType
from chess2.engine.figure import Figure


class MappingTest(unittest.TestCase):
    def test_unicode_mapping(self):
        self.assertEqual(
            FiguresMapper().map_figure_to_unicode(
                Figure(FigureType.QUEEN, FigureColor.BLACK)
            ),
            '♛',
            msg='Incorrect mapping'
        )

        self.assertNotEqual(
            FiguresMapper().map_figure_to_unicode(
                Figure(FigureType.BISHOP, FigureColor.WHITE)
            ),
            ' '
        )


    def test_svg_mapping(self):
        self.assertTrue(
            FiguresMapper().map_figure_to_svg(
                Figure(FigureType.BISHOP, FigureColor.WHITE)
            ).count('w_bishop') == 1
        )


if __name__ == '__main__':
    unittest.main()
