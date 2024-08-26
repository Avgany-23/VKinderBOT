from sqlalchemy.exc import SQLAlchemyError
from .. models import Users
from database import Session
import sqlalchemy


class UsersBd(Session):
    table = Users

    def get_one_user(self, id_vk):
        try:
            with self.session() as sess:
                return sess.query(self.table).filter_by(id_vk=id_vk).scalar()
        except SQLAlchemyError as e:
            return -1, e

    def delete_user(self, id_vk):
        try:
            with (self.session() as sess):
                sess.query(self.table).filter_by(id_vk=id_vk).delete()
                sess.commit()
                return 1
        except SQLAlchemyError as e:
            return -1

    def update_user_id(self, id_vk, new_id):
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_vk=id_vk).first()
                if user is not None:
                    user.id_vk = new_id
                    sess.commit()
                    return 1
                else:
                    return -1
        except sqlalchemy.exc.IntegrityError as e:
            return -1, e

    def create_user(self, id_vk: int) -> int:
        try:
            with self.session() as sess:
                sess.add(self.table(id_vk=id_vk))
                sess.commit()
                return 1
        except sqlalchemy.exc.IntegrityError:  # Если пользователь уже создался, то исключение
            return 0
