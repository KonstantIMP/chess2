"""
Bean management
"""
from chess2.gui.mapper import GuiMapper
from chess2.engine.mapper import FiguresMapper
from chess2.engine.chess import ChessGame
from pkg_resources import resource_filename
from chess2.model.helper import DatabaseHelper
from pathlib import Path
from sqlalchemy.orm import Session
import sqlalchemy
import typing as tp
import yaml

import asyncio

class BeanManager:
    """
    Loads config file, inits mappers and base game engine
    """
    def __init__(self):
        self.config = self.__load_config()

        self.figures_mapper = FiguresMapper()
        self.gui_mapper = GuiMapper()

        self.engine = ChessGame(self.figures_mapper)
        #self.engine.create_new_game()

        self.sql_engine = sqlalchemy.create_engine('sqlite:///games.db', echo=True)
        with self.sql_engine.begin() as connection:
            from chess2.model.base import Base
            Base.metadata.create_all(connection)

        self.session = Session(bind=self.sql_engine)

        self.helper = DatabaseHelper(self.session, self.figures_mapper)


    def __load_config(self) -> tp.Dict:
        """
        Reads and parses application.yaml
        base is used from resources and additional from
        the start directory if exist
        """
        base_config, custom_config = dict(), dict()

        with open(resource_filename('chess_2_0.resources', 'application.yaml')) as stream:
            base_config = yaml.safe_load(stream)

        if Path('application.yaml').exists():
            with open('application.yaml') as stream:
                custom_config = yaml.safe_load(stream)

        for key in custom_config:
            base_config[key] = custom_config[key]

        return base_config

