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


if __name__ == '__main__':
    unittest.main()
