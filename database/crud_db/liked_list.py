from .. models import LikedList
from database import Session
from sqlalchemy.exc import SQLAlchemyError


class LikedListBD(Session):
    table = LikedList

    def get_all_users(self, id_vk):
        """Функция достаёт все отмеченные пользователем записи"""
        try:
            with self.session() as sess:
                return sess.query(self.table).filter_by(id_user=id_vk).all()
        except SQLAlchemyError:
            return -1

    def get_all_marks_user(self, id_vk):
        """Функция достаёт все записи, где отмечен пользователь"""
        try:
            with self.session() as sess:
                return sess.query(self.table).filter_by(id_like_user=id_vk).all()
        except SQLAlchemyError:
            return -1

    def get_like_user(self, id_user, id_like_user):
        """Функция достаёт одну отмеченную пользователем запись"""
        try:
            with self.session() as sess:
                return sess.query(self.table).filter_by(id_user=id_user, id_like_user=id_like_user)
        except SQLAlchemyError:
            return -1

    def delete_like_user(self, id_user, id_like_user):
        """Функция удаляет id_vk понравившегося пользователя"""
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_user=id_user, id_like_user=id_like_user).first()
                sess.delete(user)
                sess.commit()
                return 1
        except SQLAlchemyError:
            return -1

    def delete_like_all_user(self, id_user):
        """Функция удалит все записи с LikedList.id_user = id_user"""
        try:
            with self.session() as sess:
                sess.query(self.table).filter_by(id_user=id_user).delete()
                sess.commit()
                return 1
        except SQLAlchemyError:
            return -1

    def add_like_user(self, id_user, id_like_user, name_user):
        """Функция записывает id_vk понравившегося пользователя текущему пользователю"""
        try:
            with self.session() as sess:
                sess.add(self.table(id_user=id_user,
                                    id_like_user=id_like_user,
                                    name_user=name_user))
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e
