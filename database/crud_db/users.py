from .. models import Users
from database import Session


class UsersBd(Session):
    table = Users

    def get_one_user(self, id_vk):
        """Получить одного пользователя по id_vk"""
        try:
            ...
        except:  # Указать ошибку, которая возникает в случае отсутствия указанного id в таблице Users
            ...

    def delete_user(self, id_vk):
        """Удалить пользователя по id_vk"""
        # Так же добавить блок try-except
        ...

    def update_user_id(self, id_vk):
        """Обновление id_vk у пользователя"""
        # Вряд ли понадобится, но можно написать для полноценного диапазона запросов
        ...

    def create_user(self, id_vk):
        """Создать пользователя по id_vk"""
        # Добавить try-expect, чтобы не вылезало ошибки при повторном создании одного и того же пользователя
        with self.session() as sess:
            sess.add(self.table(id_vk=id_vk))
            sess.commit()