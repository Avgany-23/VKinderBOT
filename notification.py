from vk_bot.bot_function import *
from settings import VK_KEY_API
from database import session_bd, PATH
from database.models import SearchPeople
from database.models import Users, SearchPeople
from database.crud_db.search_people import SearchPeopleBd
from api_vk.main import SearchVK
from database.crud_db.filters_users import UsersFiltersBd
from database.crud_db.info_users import InfoUsersBd
from database.crud_db.liked_list import LikedListBD
from database.crud_db.black_list import BlackListBD
from database.crud_db.users import UsersBd
# print(search_people_and_save(240353515))
# print(search(240353515, VK_KEY_API))
print(SearchVK(VK_KEY_API).get_user_vk(240353515))

# filters = UsersFiltersBd()
# print(filters.get_filters_user(240353515).age_to)

# user = SearchPeopleBd()
# user_id = user.get_user(240353515).id_user
#
# info = SearchVK(VK_KEY_API)
# print(info.get_user_vk(user_id))


# Взять первого пользователя из БД для показа:
# session = session_bd(PATH)
# session = session()
# user = session.query(Users.id_vk, SearchPeople.id_user).join(SearchPeople, SearchPeople.id_user_main == Users.id_vk).first()
# print(user)


# user = get_message_search(240353515)


# search = SearchVK(VK_KEY_API)
# user_info = search.get_photo_user(240353515)
# print(user_info)

users_bd = UsersBd()
info_users_bd = InfoUsersBd()
liked_list_bd = LikedListBD()
black_list_bd = BlackListBD()
#Test_add_dell_user
id_vk = 1000001
old_id = 2000000
new_id = 1000000
test_one_id = 1234537
#Test_info_user
id_user = 1234537
name = "Ловелас"
age = 21
gender = "мужской"
marital_status = "активный поиск"
city = "Москва"
interests = "Музыка"
#Test_liked_list
id_user = 1234537
id_like_user = 999
#Test_black_list
id_user = 1234537
id_ignore_user = 888