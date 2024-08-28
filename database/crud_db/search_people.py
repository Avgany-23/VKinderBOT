from sqlalchemy.exc import SQLAlchemyError
from database.models import SearchPeople
from database import Session


class SearchPeopleBd(Session):
    table = SearchPeople

    def add_user(self, id_user_main: int, id_user: int):
        """Функция для сохранения человека для отображения пользователю id_user_main"""
        try:
            with self.session() as sess:
                sess.add(self.table(id_user_main=id_user_main, id_user=id_user))
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e

    def add_users(self, id_user_main: int, id_users: list):
        """Функция для нескольких людей для отображения пользователю id_user_main"""
        try:
            with self.session() as sess:
                result = [self.table(id_user=id_, id_user_main=id_user_main) for id_ in id_users]
                sess.add_all(result)
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e

    def get_user(self, id_user_main: int):
        """Получить информацию о первом найденном пользователе по id_user_main"""
        try:
            with self.session() as sess:
                return sess.query(self.table).filter_by(id_user_main=id_user_main).first()
        except SQLAlchemyError as e:
            return -1, e

    def delete_user(self, id_user_main: int, id_users: int):
        """Удаление одной записи у пользователя id_user_main"""
        try:
            with self.session() as sess:
                sess.query(self.table).filter_by(id_user=id_users, id_user_main=id_user_main).delete()
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e

    def delete_user_all(self, id_user_main: int):
        """Удаление всех записей у пользователя id_user_main"""
        try:
            with self.session() as sess:
                sess.query(self.table).filter_by(id_user_main=id_user_main).delete()
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e