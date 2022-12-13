"""
Helper для работы с базой данных
"""
from sqlalchemy.orm import Session
from uuid import uuid4
from chess2.engine.chess import ChessGame
from chess2.engine.figure_color import FigureColor
from chess2.model.games import Game
from chess2.model.step import Step as DbStep
from chess2.engine.mapper import FiguresMapper
import typing as tp

class DatabaseHelper:
    """Сохраняет/загружает игровые партии"""
    def __init__(self, session: Session, mapper: FiguresMapper):
        self.session = session
        self.mapper = mapper


    def save_game(self, game: ChessGame, name: str) -> None:
        """Сохраняет текущую партия в базу данных с указанным именем"""
        obj = Game(
            uid=str(uuid4()),
            name=name,
            last_color='white' if game.current_color == FigureColor.WHITE else 'black'
        )
        self.session.add(obj)

        for i, step in enumerate(game.history):
            item = DbStep(
                number=i,
                a=self.mapper.map_position(step.a),
                b=self.mapper.map_position(step.b),
                game_id=obj.uid
            )
            self.session.add(item)

        self.session.commit()


    def get_saved_games(self) -> tp.List[str]:
        """Возвращает список сохраненных партий"""
        return list(map(lambda x: x.name, self.session.query(Game).all()))


    def load_game(self, n: str, game: ChessGame) -> None:
        """загружает партию из БД по ее имени"""
        obj: Game = self.session.query(Game).filter(Game.name == n).one()
        steps: tp.List[DbStep] = self.session.query(DbStep).filter(DbStep.game_id == obj.uid).all()
        steps.sort(key=lambda x: x.number)

        game.create_new_game()

        for step in steps:
            game.make_step(
                self.mapper.map_to_position(step.a),
                self.mapper.map_to_position(step.b)
            )


    def delete_game(self, n: str) -> None:
        """Удаляет партию из БД"""
        obj: Game = self.session.query(Game).filter(Game.name == n).one()

        self.session.query(DbStep).filter(DbStep.game_id == obj.uid).delete()
        self.session.query(Game).filter(Game.uid == obj.uid).delete()

        self.session.commit()

