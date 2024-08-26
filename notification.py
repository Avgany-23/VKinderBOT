# Модуль для уведомлений


from database.crud_db.users import UsersBd
from database.crud_db.liked_list import LikedList
from random import randrange
from database.models import Users, LikedList
from database import session_bd, PATH
from api_vk.main import SearchVK


import re
# bd = UsersBd()
# user = bd.create_user(141)
# print(user)


# session = session_bd(PATH)()
# user = session.query(LikedList).filter_by(id_user=123).all()
# print(user)
# like = LikedList(id_like_user=1)
# user.likedlist = like
# session.add(user)
# session.commit()



# def decor(a):
#     def decor_a(func):
#         def wrapper(*args, **kwargs):
#             print(a)
#             return func(*args, **kwargs)
#         return wrapper
#     return decor_a
#
# def func(a):
#     return a
#
# print(decor(5)(func)(1))
#

from api_vk.main import SearchVK
from settings import VK_KEY_API
from datetime import datetime


def calculate_age(date_):
    birthday = datetime.strptime(date_, '%d.%m.%Y')
    today = datetime.now()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def filter_age(birth_date):
    age = calculate_age(birth_date)
    if age > 50:
        return 50, 80
    return age, age + 5


vk_user = SearchVK(VK_KEY_API)
user = vk_user.get_user_vk(240353515)
photo = vk_user.get_photo_user(240353515, 'profile')
# print(photo)
# info = user
# print(info)
# info['sex'] = 1 if info['sex'] == 2 else 2
# range_age = filter_age(info['bdate'])
# result = {'sex': info['sex'], 'age_from': range_age[0], 'age_to': range_age[1], 'city_id': info['city_id'], 'city_title': info['city_title'], 'relation': info['relation']}
# print(result)


# print(re.findall(r'(\d{1,})[- ](\d{1,})', 'Установить возраст: 10 20'))

print()









# result = UsersBd().create_user(228)
# print(result)


# user_info1 = vk_user.get_users_vk(city=5, count=1000)
# user_info2 = vk_user.get_users_vk(count=1000)
# print(len(user_info1), len(user_info2))
# for el in user_info1[-3:]:
#     print(el)
# print()
# for el in user_info2[-3:]:
#     print(el)





# users = bd.get_all()
# for i in users:
#     print(i.id_vk)

# for id in range(10):                    # Тест создания юзеров
#     bd.create_user(randrange(10000))

# users = bd.get_all()                    # Тест проверки метода get_all()
# print(next(users).id_vk)
# print(next(users).id_vk)
# print(next(users).id_vk)
# print(next(users).id_vk)
