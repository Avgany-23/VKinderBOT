from vk_bot.bot_function import *
from settings import VK_KEY_API
from database import session_bd, PATH
from database.models import SearchPeople
from database.models import Users, SearchPeople, LikedList, BlackList
from database.crud_db.search_people import SearchPeopleBd
from api_vk.main import SearchVK
from database.crud_db.filters_users import UsersFiltersBd
from sqlalchemy import join, outerjoin


# .filter_by(Users.id_vk == 240353515)
session = session_bd(PATH)
with session() as sess:
    result = (sess.query(Users.id_vk, LikedList.id_like_user, BlackList.id_ignore_user).
              join(BlackList, Users.id_vk == BlackList.id_user).
              outerjoin(LikedList, Users.id_vk == LikedList.id_user).
              filter(Users.id_vk == '240353515')).all()
    # result = joined.outerjoin(LikedList, Users.id_vk == LikedList.id_user).all()
    print(result)
    # for i in result:
    #     print(i)









# print(search_people_and_save(240353515))
# print(search(240353515, VK_KEY_API))
# print(SearchVK(VK_KEY_API).get_user_vk(240353515))

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

