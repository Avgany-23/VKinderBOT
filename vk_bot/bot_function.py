from database.crud_db import  liked_list, black_list
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard
from database.crud_db.filters_users import UsersFiltersBd
from database.crud_db.liked_list import LikedListBD
from typing import Optional
from vk_api import VkApi
from .utils import (choose_plural,
                    correct_size_photo,
                    get_photo_vk_id,
                    carousel_str)
import re


def send_message(vk: VkApi,
                 user_id: int,
                 message: str,
                 keyboard: Optional[VkKeyboard] = None,
                 template: str = None) -> None:
    """Отправка сообщения ботом в чат"""
    values = {
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id()
    }
    if keyboard:
        values['keyboard'] = keyboard.get_keyboard()
    if template:
        values['template'] = template

    vk.method('messages.send', values)


def snow_snackbar(vk: VkApi, event_id: str, user_id: int, peer_id: int, event_data: str):
    """Отправка всплывающего сообщения"""
    values = {
        'event_id': event_id,
        'user_id': user_id,
        'peer_id': peer_id,
        'event_data': event_data
    }
    vk.method('messages.sendMessageEventAnswer', values)


def list_users(id_vk: int, count: int = 15, list_user: str = 'Like list') -> str:
    """
    Возвращает count пользователей из БД.
    list_user: like_pages - из таблицы LikedList, block_pages - из таблицы BlackList
    """
    query = liked_list.LikedListBD() if list_user == 'like list' else black_list.BlackListBD()
    result = query.get_all_users(id_vk)
    if not result:
        return 'Список пуст'
    message = choose_plural(count, ('отмеченный', 'отмеченных', 'отмеченных') if list_user == 'like list'
                            else ('игнорируемый', 'игнорируемых', 'игнорируемых'))
    count_user = len(result) if len(result) < count else count
    return f"{'Список' if count > 2 else ''} {count_user} {message[1]} вами пользователей: {result}"


def browsing_history(count):
    """Из таблицы с историей просмотров достает последние count записей"""
    return 'Ваша история просмотров: %s' % count


def user_filters(id_user: int) -> str:
    """Возвращает описание пользовательских фильтров"""
    filters = UsersFiltersBd().get_filters_user(id_user)
    status = {
        0: 'неважно',
        1: 'не женат (не замужем)',
        2: 'встречается',
        3: 'помолвлен(-а)',
        4: 'женат (замужем)',
        5: 'всё сложно',
        6: 'в активном поиске',
        7: 'влюблен(-а)',
        8: 'в гражданском браке'
    }
    result_filters = (f'Город: {filters.city_title}\n'
                      f'Возраст: {filters.age_from}-{filters.age_to}\n'
                      f'Статус отношений: {status[filters.relation]}')
    return (f'Текущие фильтры поиска людей:\n{result_filters}\n'
            f'Для установки своего возраста написать:\nУстановить возраст: от-до\n')


def get_template_carousel(vk, path) -> str:
    result_photos = []
    for el in path:
        correct_size_photo(el)
        result_photos.append(get_photo_vk_id(el, vk))

    return carousel_str(result_photos)


def change_filter_age(id_vk: int, age: str) -> None:
    """Принимает строку age в формате XX-XX или XX XX или >35 и обновляет запись в таблице UsersFiltersBd"""
    if age == '>35':
        age_from, age_to = 35, 100
    else:
        age = re.findall(r'(\d{1,})[- ](\d{1,})', age)
        age_from, age_to = int(age[0][0]), int(age[0][1])
    UsersFiltersBd().update_filters_user(id_vk=id_vk, age_from=age_from, age_to=age_to)


def change_filter_sex(id_vk: int, sex: str) -> None:
    """Изменяет фильтр """
    sex_ = {'женский': 1, 'мужской': 2}
    UsersFiltersBd().update_filters_user(id_vk=id_vk, sex=sex_[sex])


def marks_person(id_vk: int) -> str:
    """Функция вычисляет, сколько людей отметило пользователя с id_vk"""
    mark_person = len(LikedListBD().get_all_marks_user(id_vk))
    message = choose_plural(mark_person, ('человек', 'человека', 'человек'))
    return f"{message[0]} {message[1]}"