from sqlalchemy.exc import SQLAlchemyError
from .. models import BlackList
from database import Session


class BlackListBD(Session):
    table = BlackList

    def get_all_users(self, id_vk: int):
        try:
            with self.session() as sess:
                return sess.query(self.table).filter_by(id_user=id_vk).all()
        except SQLAlchemyError as e:
            return -1, e

    def delete_user_black_list(self, id_user: int, id_ignore_user: int):
        try:
            with self.session() as sess:
                sess.query(self.table).filter_by(id_user=id_user, id_ignore_user=id_ignore_user).delete()
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e

    def add_user_black_list(self, id_user: int, id_ignore_user: int):
        try:
            with self.session() as sess:
                sess.add(self.table(id_user=id_user, id_ignore_user=id_ignore_user))
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1, e