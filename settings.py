from dotenv import load_dotenv
import os


load_dotenv()

# Токен от ВК бота:
TOKEN_BOT = os.getenv('token_bot2')

# ID группы ВК, в которой находится БОТ:
GROUP_ID_VK = int(os.getenv('group_id'))

# Токен от VK-API:
VK_KEY_API = os.getenv('vk_api_key')

# Версия API-VK
VK_VERSION = '5.199'  # Добавить её во все классы

DATABASES = {
    'postgresql': {
        'NAME': 'postgresql',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
        'BD_NAME': 'vk',
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'decode_responses': True,
        'charset': "utf-8",
    }
}