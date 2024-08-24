from database.models import Users
from database import Session
from info_users import InfoUsersBd

class UsersBd(Session):
    table = Users

    def get_one_user(self, id_vk):
        """Получить одного пользователя по id_vk из модуля info_users"""
        info_users_bd = InfoUsersBd()
        result = info_users_bd.get_one_user(id_vk)
        return result

    def delete_user(self, id_vk):
        """Удалить пользователя по id_vk"""
        # Добавлен try-expect - обход ошибки при попытке удалить несуществующего пользователя
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_vk=id_vk).first()
                sess.delete(user)
                sess.commit()
                return 1
        except Exception as e:
            # информация об ошибке е не передаю
            return -1


    def update_user_id(self, id_vk, new_id):
        """Обновление id_vk у пользователя"""
        try:
            with self.session() as sess:
                user = sess.query(self.table).filter_by(id_vk=id_vk).first()
                if user is not None:
                    user.id_vk = new_id
                    sess.commit()
                    return 1
                else:
                    return -1
        except Exception as e:
            # Информация об ошибке e не передается
            return -1


    def create_user(self, id_vk):
        """Создать пользователя по id_vk"""
        # Добавлен try-expect - обход ошибки при попытке добавить пользователя повторно
        try:
            with self.session() as sess:
                sess.add(self.table(id_vk=id_vk))
                sess.commit()
                return 1
        except Exception as e:
            # информация об ошибке е не передаю
            return -1
