from dotenv import load_dotenv
import os


load_dotenv()

# Токен от ВК бота:
TOKEN_BOT = os.getenv('token_bot')

# ID группы ВК, в которой находится БОТ:
GROUP_ID_VK = int(os.getenv('group_id'))

# Токен от VK-API:
VK_KEY_API = os.getenv('vk_api_key')

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