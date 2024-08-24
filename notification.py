# Модуль для уведомлений
from database.crud_db.users import UsersBd
from random import randrange


bd = UsersBd()

for id in range(10):                    # Тест создания юзеров
    bd.create_user(randrange(10000))

# users = bd.get_all()                    # Тест проверки метода get_all()
# print(next(users).id_vk)
# print(next(users).id_vk)
# print(next(users).id_vk)
# print(next(users).id_vk)
