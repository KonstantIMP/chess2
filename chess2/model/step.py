"""
Описание одного хода в БД
"""
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from chess2.model.games import Game
from chess2.model.base import Base


class Step(Base):
    __tablename__ = 'steps'

    number = Column(Integer)
    a = Column(String)
    b = Column(String)
    game_id = Column(String, ForeignKey('games.uid'))

    id = Column(Integer, primary_key=True, autoincrement=True)
