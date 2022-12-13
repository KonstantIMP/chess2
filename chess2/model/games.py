"""
Описание Игры для хранения в бд
"""
from sqlalchemy import Column, Integer, String
from chess2.model.base import Base


class Game(Base):
    __tablename__ = 'games'
    
    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    last_color = Column(String, nullable=False)
