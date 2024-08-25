# Для общих настроек проекта.
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN_BOT = os.getenv('token_bot')
GROUP_ID_VK = int(os.getenv('group_id'))
VK_KEY_API = None

DATABASES = {
    'postgresql': {
        'NAME': 'postgresql',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
        'BD_NAME': 'vk',
    }
}

