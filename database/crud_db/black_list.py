from sqlalchemy.exc import SQLAlchemyError
from database.models import BlackList
from database import Session


class BlackListBd(Session):
    table = BlackList

    def add_black_list(self, id_user, id_ignore_user):
        """Функция записывает id_vk блокируемого пользователя"""
        # Использую контекстный менеджер для работы с сессией
        try:
            with self.session() as sess:
                """Добавляем информацию о пользователях"""
                sess.add(self.table(id_user=id_user,
                                   id_ignore_user=id_ignore_user))
                """Фиксируем изменения в базе данных"""
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            # информация об ошибке е не передаю
            return -1


    def get_black_list(self, id_user, id_ignore_user):
        """Функция удаляет id_vk понравившегося пользователя"""
        # Использую контекстный менеджер для работы с сессией
        try:
            with self.session() as sess:
                user = sess.query(self.table.id_user,
                                  self.table.id_ignore_user).filter_by(
                    id_user=id_user, id_ignore_user=id_ignore_user).first()
                if user is not None:
                    return user
                else:
                    return -1  # Пользователь с таким id не найден
        except SQLAlchemyError as e:
            return -1


    def dell_black_list(self, id_user, id_ignore_user):
        """Функция удаляет id_vk заблокированого ранее пользователя"""
        # Использую контекстный менеджер для работы с сессией
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_user=id_user, id_ignore_user=id_ignore_user).first()
                sess.delete(user)
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            # информация об ошибке e передаю 2м
            return -1, e