from sqlalchemy.exc import SQLAlchemyError
from database.models import FiltersUsers
from database import Session


class UsersFiltersBd(Session):
    table = FiltersUsers

    def add_filters_users(self, id_user, **kwargs):
        """Функция для записи информации о фильтрах пользователя"""
        try:
            with self.session() as sess:
                sess.add(self.table(id_user=id_user, **kwargs))
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e

    def get_filters_user(self, id_vk):
        """Получить фильтры одного пользователя по id_vk"""
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_user=id_vk).first()
                if user is not None:
                    return user
                else:
                    return -1  # Пользователь с таким id не найден
        except SQLAlchemyError as e:
            return -1, e

    def update_filters_user(self, id_vk, **kwargs):
        """Изменение фильтров пользователя"""
        with self.session() as sess:
            try:
                sess.query(self.table).filter_by(id_user=id_vk).update(kwargs)
                sess.commit()
                return 1
            except SQLAlchemyError as e:
                return -1, e
