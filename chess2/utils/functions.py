"""
Набор необходимых функций
"""
import typing as tp

# Любой тип, но одинаковый для аргументов и возвращаемого значения
T = tp.TypeVar('T')


def flatten(l: tp.List[tp.List[T]]) -> tp.List[T]:
    """
    Переводит матрицу (список списков) в вектор (склеивание по строкам)
    """
    return [item for sublist in l for item in sublist]

