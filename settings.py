from dotenv import load_dotenv
import os


load_dotenv()

# Токен от ВК бота:
TOKEN_BOT = os.getenv('token_bot')

# ID группы ВК, в которой находится БОТ:
GROUP_ID_VK = os.getenv('group_id')

# Токен от VK-API:
VK_KEY_API = os.getenv('vk_api_key')

# Версия API-VK
VK_VERSION = '5.199'

# Размер кеша для сохранения истории просмотров анкет
HISTORY_SIZE = 15

# Базы данных
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

# Для Telegram Бота (отправка логов). По умолчанию выключен - include = False. include = True - включить
tg_bot = {
    'include': True,    # True - бот работает (нужны будут данные к нему из файла .env), False - выключен
    'data': {
        'token': os.getenv('bot_tg'),
        'login': '1234',
        'password': '1234',
    },
    # Время указывается в формате HH:MM без секунд для корректной отправки уведомлений
    'send_times': [
        '12:00',
        '21:07',
        '02:00',
    ]
}
