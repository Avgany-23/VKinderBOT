from database.create_bd import create_bd_and_tables_if_not_exists
from logs.logs import logger_error, logger_starts_program
from vk_bot_main import vk_bot_main
from settings import tg_bot
from vk_api import vk_api
from typing import Union
import redis.exceptions


# ------------------ Create DataBase if it exists
result = create_bd_and_tables_if_not_exists()


if result == -3:
    logger_error.error('При запуске программы неправильно указаны данные при подключении к PostgreSQL')

if result == -2:
    logger_starts_program.info('При запуске программы база данных PostgreSQL создана, но таблицы в ней уже существуют')

if result == -1:
    logger_starts_program.info('При запуске программы база данных PostgreSQL и таблицы в ней уже существуют. '
                               'Их создание не произошло.')

if result == 1:
    logger_starts_program.info('Запуск программы. База данных и таблицы в ней созданы.')


# ------------------ Start TG bot, if tg_bot['include'] is True at the settings.py
if tg_bot['include']:
    import threading
    from logs.tg_bot import bot_notification_tg
    threading.Thread(target=bot_notification_tg).start()


# ------------------ Start VK bot
def vk_bot_main_recursive() -> Union[None, 'vk_bot_main_recursive']:
    try:
        vk_bot_main()

    except vk_api.ApiError:
        logger_error.error('Что-то пошло не так. Вероятно, слетел токен от ВК бота/неверно указан id токена/'
                           'неверно указано id группы vk. VK bot остановлен.\n ')
        return None

    except redis.exceptions.ConnectionError:
        logger_error.error('Не удалось подключиться к редису. VK bot остановлен.\n ')
        return None

    except BaseException as e:
        logger_error.error(f'Что-то пошло не так. Вероятно, ошибка из-за токена Апи-ВК.\n '
                           f'Конкретная причина ошибки:\n{e}')
    vk_bot_main_recursive()

vk_bot_main_recursive()
