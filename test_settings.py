from database.crud_db.filters_users import UsersFiltersBd
from database.crud_db.search_people import SearchPeopleBd
from database.crud_db.black_list import BlackListBD
from database.crud_db.info_users import InfoUsersBd
from database.crud_db.liked_list import LikedListBD
from database.crud_db.users import UsersBd
from database import session_bd
from dotenv import load_dotenv
import os


load_dotenv()

DATABASES_TEST = {
    'postgresql': {
        'NAME': 'postgresql',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
        'BD_NAME': 'vk_test',
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 1,
        'decode_responses': True,
        'charset': "utf-8",
    }
}

DT_POSTGRESQL = DATABASES_TEST['postgresql']
PATH_TEST_POSTGRESQL = (f"{DT_POSTGRESQL['NAME']}://{DT_POSTGRESQL['USER']}:{DT_POSTGRESQL['PASSWORD']}@"
                        f"{DT_POSTGRESQL['HOST']}:{DT_POSTGRESQL['PORT']}/{DT_POSTGRESQL['BD_NAME']}")

# Токен от ВК бота:
TOKEN_BOT_TEST = os.getenv('token_bot_test')

# ID группы ВК, в которой находится БОТ:
GROUP_ID_VK_TEST = int(os.getenv('group_id_test'))

# Токен от VK-API:
VK_KEY_API_TEST = os.getenv('vk_api_key_test')

# id пользователя в ВК, с которым будет взаимодействовать бот для тестов
VK_ID_TEST = os.getenv('id_vk_for_test')


# Тестовое подключение запросов к БД:
session_test = session_bd(PATH_TEST_POSTGRESQL)

test_BlackListBD = BlackListBD()
test_UsersFiltersBd = UsersFiltersBd()
test_InfoUsersBd = InfoUsersBd()
test_LikedListBD = LikedListBD()
test_SearchPeopleBd = SearchPeopleBd()
test_UsersBd = UsersBd()

test_BlackListBD.session = session_test
test_UsersFiltersBd.session = session_test
test_InfoUsersBd.session = session_test
test_LikedListBD.session = session_test
test_SearchPeopleBd.session = session_test
test_UsersBd.session = session_test
