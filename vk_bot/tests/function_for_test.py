from test_settings import test_BlackListBD, test_LikedListBD
from database.create_bd import create_object_db, check_bd, create_bd
from vk_api.bot_longpoll import VkBotLongPoll
from vk_bot.bot_function import send_message
from vk_bot.utils import choose_plural
from vk_api import VkApi
import vk_api


def test_connect_vk_bot(token_bot: str, group_id_vk: str, vk_id_user: int) -> bool:
    """--- Тестовое подключение ВК боту и проверка подключения ---"""
    result_connect = True
    try:
        vk = VkApi(token=token_bot)
        vk.get_api()
        VkBotLongPoll(vk, group_id_vk)
        send_message(vk=vk, user_id=vk_id_user, message='--- START TEST ---')
    except vk_api.exceptions.ApiError:
        print('Неправильно указаны данные token_bot_test/group_id_test/id_vk_for_test\n'
              'Часть тестов пропускается')
        result_connect = False

    return result_connect


def test_create_bd(path: str) -> bool:
    """--- Подключение к тестовой БД, создание БД и таблиц и проверка ---"""
    create_bd_status = True
    result_db = create_object_db(path)
    if result_db[0] != 1:
        create_bd_status = False
        print(f'База данных не создана {create_bd_status=}. Часть функций протестирована не будет')
    else:
        try:
            check_bd(path)
        except SystemError:
            create_bd_status = False
            print(f'Таблицы не созданы {create_bd_status=}. Часть функций протестирована не будет')
        else:
            create_bd(path)
    return create_bd_status


def list_users_test(id_vk: int, list_user: str = 'like list') -> str:
    """
    Возвращает  пользователей из БД.
    list_user: like_pages - из таблицы LikedList, block_pages - из таблицы BlackList
    """
    list_user = list_user.lower()
    query = test_LikedListBD if list_user == 'like list' else test_BlackListBD

    result = query.get_all_users(id_vk)

    if list_user == 'like list':
        message = choose_plural(len(result), ('отмеченный', 'отмеченных', 'отмеченных'))
    else:
        message = choose_plural(len(result), ('игнорируемый', 'игнорируемых', 'игнорируемых'))

    if not result:
        return 'Список пуст'

    if list_user == 'like list':
        people = '\n'.join(f"{i})Имя: {person.name_user} | "
                           f"{'https://vk.com/id'+str(person.id_like_user)}" for i, person in enumerate(result, 1))
    else:
        people = '\n'.join(f"{i})Имя: {person.name_user} | "
                           f"{'https://vk.com/id'+str(person.id_ignore_user)}" for i, person in enumerate(result, 1))

    return f"{'Список' if len(result) > 2 else ''} {len(result)} {message[1]} вами пользователей:\n{people}"
