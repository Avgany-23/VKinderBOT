from database.models import InfoUsers
from database import Session

class InfoUsersBd(Session):
    table = InfoUsers

    def info_users(self, id_user,
                   name=None,
                   age=None,
                   gender=None,
                   marital_status=None,
                   city=None,
                   interests=None):
        """Функция для записи информации о пользователе"""
        #Использую контекстный менеджер для работы с сессией
        try:
            with self.session() as sess:
                """Добавляем информацию о пользователе"""
                sess.add(InfoUsers(id_user=id_user,
                                      name=name,
                                      age=age,
                                      gender=gender,
                                      marital_status=marital_status,
                                      city=city,
                                      interests=interests
                                      ))
                """Фиксируем изменения в базе данных"""
                sess.commit()
                return 1
        except Exception as e:
        # информация об ошибке е не передаю
            return -1

    def get_one_user(self, id_vk):
        """Получить одного пользователя по id_vk"""
        try:
            with self.session() as sess:
                user = sess.query(self.table.id_user,
                                  self.table.name,
                                  self.table.age,
                                  self.table.gender,
                                  self.table.marital_status,
                                  self.table.city,
                                  self.table.interests).filter_by(
                    id_user=id_vk).first()
                if user is not None:
                    return user
                else:
                    return -10  # Пользователь с таким id не найден
        except Exception as e:
            return -12

