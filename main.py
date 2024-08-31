from database.create_bd import create_bd_and_tables_if_not_exists
from vk_bot_main import vk_bot_main
from settings import tg_bot
from vk_api import vk_api

# Create DataBase if it exists
create_bd_and_tables_if_not_exists()


# Start TG bot, if tg_bot['include'] is True at the settings.py
if tg_bot['include']:
    import threading
    from logs.tg_bot import bot_notification_tg
    threading.Thread(target=bot_notification_tg).start()


# Start VK bot
try:
    vk_bot_main()
except vk_api.ApiError:
    print('Лог: что-то пошло не так. Вероятно, слетел токен от ВК бота\n'
          'или значение токена/id_group_vk неверное')
except BaseException as e:
    print(f'Лог: что-то пошло не так. Вероятно, ошибка из-за токена Апи-ВК. Причина ошибки:\n{e}')
