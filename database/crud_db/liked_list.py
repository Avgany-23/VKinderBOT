from sqlalchemy.exc import SQLAlchemyError
from database.models import LikedList
from database import Session


class LikedListBb(Session):
    table = LikedList

    def add_like_user(self, id_user, id_like_user):
        """Функция записывает id_vk понравившегося пользователя
        текущему пользователю"""
        # Использую контекстный менеджер для работы с сессией
        try:
            with self.session() as sess:
                """Добавляем информацию о пользователях"""
                sess.add(self.table(id_user=id_user,
                                   id_like_user=id_like_user))
                """Фиксируем изменения в базе данных"""
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            # информация об ошибке е не передаю
            return -1


    def get_like_user(self, id_user, id_like_user):
        """Функция удаляет id_vk понравившегося пользователя"""
        # Использую контекстный менеджер для работы с сессией
        try:
            with self.session() as sess:
                user = sess.query(self.table.id_user,
                                  self.table.id_like_user).filter_by(
                    id_user=id_user, id_like_user=id_like_user).first()
                if user is not None:
                    return user
                else:
                    return -1  # Пользователь с таким id не найден
        except SQLAlchemyError as e:
            return -1


    def dell_like_user(self, id_user, id_like_user):
        """Функция удаляет id_vk понравившегося пользователя"""
        # Использую контекстный менеджер для работы с сессией
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_user=id_user, id_like_user=id_like_user).first()
                sess.delete(user)
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            # информация об ошибке е не передаю
            return -1