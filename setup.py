"""
  Setup file for the Chess 2.0 project
"""
from setuptools import find_packages, setup
from pathlib import Path
import typing as tp


def read_requirements(path: str) -> tp.List[str]:
    """
    Reads file from 'path' in requirements.txt format
    and creates list of dependencies from it

    Parameters
    ----------
    path : str, required
        Path to the file with requirements list
    """
    comment_identifiers = ('"', '#', '-', 'git+')

    with open(path, 'r') as requirements:
        return list(
            filter(
                lambda x: not x.startswith(comment_identifiers),
                map(str.strip, requirements.readlines())
            )
        )


def read_version(path: str) -> str:
    """
    Reads file from 'path' and gets the project's version from it

    Parameters
    ----------
    path : str, required
        Path to the file with the projetc's version
    """
    return open(path, 'r').read().strip()


sources_dir = Path('.') / 'chess2'

setup(
    name='chess2',
    version=read_version(str(sources_dir / 'VERSION')),
    description='Chess 2.0 - just a chess in python',
    author='KonstantIMP',
    author_email='konstantimp@ya.ru',
    packages=['chess2', 'chess2.engine', 'chess2.gui', 'chess2.resources', 'chess2.model', 'chess2.utils'],
    package_data={'': ['*.svg', '*.yaml']},
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': ['chess2 = chess2.__main__:main']
    }
)
