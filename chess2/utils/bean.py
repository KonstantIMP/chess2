"""
Менеджер элементов (бинов)
"""
from chess2.gui.mapper import GuiMapper
from chess2.engine.mapper import FiguresMapper
from chess2.engine.chess import ChessGame
from chess2.model.helper import DatabaseHelper
from chess2.model.base import Base
from pkg_resources import resource_filename
from pathlib import Path
from sqlalchemy.orm import Session
import sqlalchemy
import typing as tp
import yaml


class BeanManager:
    """
    Загружает конфигурационный файл, подключается к БД и
    инициализирует мапперы
    """
    def __init__(self):
        self.config = self.__load_config()

        self.figures_mapper = FiguresMapper()
        self.gui_mapper = GuiMapper()

        self.engine = ChessGame(self.figures_mapper)

        self.sql_engine = sqlalchemy.create_engine('sqlite:///games.db', echo=True)
        with self.sql_engine.begin() as connection:
            Base.metadata.create_all(connection)

        self.session = Session(bind=self.sql_engine)

        self.helper = DatabaseHelper(self.session, self.figures_mapper)


    def __load_config(self) -> tp.Dict:
        """
        Читает и парсит application.yaml из подпакета
        с ресурсами и переписывает некоторые параметры из локального
        конфига, если он существует
        """
        base_config, custom_config = dict(), dict()

        with open(resource_filename('chess2.resources', 'application.yaml')) as stream:
            base_config = yaml.safe_load(stream)

        if Path('application.yaml').exists():
            with open('application.yaml') as stream:
                custom_config = yaml.safe_load(stream)

        for key in custom_config:
            base_config[key] = custom_config[key]

        return base_config

