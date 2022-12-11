"""
Come useful functions
"""
import typing as tp


T = tp.TypeVar('T')


def flatten(l: tp.List[tp.List[T]]) -> tp.List[T]:
    """
    Converts list of lists (matrix) to list (vector)
    """
    return [item for sublist in l for item in sublist]
