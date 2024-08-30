from sqlalchemy.exc import SQLAlchemyError
from database.models import InfoUsers
from database import Session


class InfoUsersBd(Session):
    table = InfoUsers

    def add_info_users(self, id_user, **kwargs):
        """Функция для записи информации о пользователе"""
        try:
            with self.session() as sess:
                sess.add(self.table(id_user=id_user, **kwargs))
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e

    def get_info_user(self, id_vk):
        """Получить информацию одного пользователя по id_vk"""
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_user=id_vk).first()
                if user is not None:
                    return user
                else:
                    return -1  # Пользователь с таким id не найден
        except SQLAlchemyError as e:
            return -1, e
