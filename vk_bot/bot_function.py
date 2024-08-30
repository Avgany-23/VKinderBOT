from database.crud_db.filters_users import UsersFiltersBd
from database.crud_db.search_people import SearchPeopleBd
from database.crud_db.black_list import BlackListBD
from database.crud_db.liked_list import LikedListBD
from database.models import Users, SearchPeople
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard
from database import session_bd, PATH
from api_vk.main import SearchVK
from settings import VK_KEY_API
from typing import Optional
from random import shuffle
from vk_api import VkApi
from .utils import (
    choose_plural,
    calculate_age,
    message_status,
    message_city
)
import re


def send_message(vk: VkApi,
                 user_id: int,
                 message: str,
                 keyboard: Optional[VkKeyboard] = None,
                 template: str = None,
                 attachment: list = None) -> None:
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
    if attachment:
        values['attachment'] = attachment

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


def list_users(id_vk: int, list_user: str = 'Like list') -> str:
    """
    Возвращает count пользователей из БД.
    list_user: like_pages - из таблицы LikedList, block_pages - из таблицы BlackList
    """

    query = LikedListBD() if list_user == 'like list' else BlackListBD()
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


def user_filters(id_user: int) -> str:
    """Возвращает описание пользовательских фильтров"""
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
    filters = UsersFiltersBd().get_filters_user(id_user)
    result_filters = (f'Город: {filters.city_title}🌇\n'
                      f'Возраст: {filters.age_from}-{filters.age_to}❗\n'
                      f'Пол: {"мужской 👦" if filters.sex == 2 else "женский 👧"}\n'
                      f'Статус отношений: {status[filters.relation]}📓\n')
    return (f'Текущие фильтры поиска людей:\n{result_filters}\n'
            f'Для установки своего возраста написать:\nУстановить возраст: от-до\n')


def change_filter_age(id_vk: int, age: str) -> None:
    """Принимает строку age в формате XX-XX или XX XX или >35 и обновляет запись в таблице UsersFiltersBd"""
    if age == '>35':
        age_from, age_to = 35, 100
    else:
        age = re.findall(r'(\d+)[- ](\d+)', age)
        age_from, age_to = int(age[0][0]), int(age[0][1])
    UsersFiltersBd().update_filters_user(id_vk=id_vk, age_from=age_from, age_to=age_to)


def change_filter_sex(id_vk: int, sex: str) -> None:
    """Изменяет фильтр пола"""
    sex_ = {'женский': 1, 'мужской': 2}
    UsersFiltersBd().update_filters_user(id_vk=id_vk, sex=sex_[sex])


def change_filter_status(id_vk: int, status: str) -> str:
    """Изменяет фильтр статуса"""
    active_status = message_status()[0]
    if int(status[-1]) in active_status:
        UsersFiltersBd().update_filters_user(id_vk=id_vk, relation=status[-1])
        return 'Статус установлен'
    else:
        return 'Такой статус не доступен'


def change_filter_city(id_vk: int, city: str) -> str:
    """Изменяет фильтр города"""
    city = int(re.findall(r'\d+', city)[0])
    all_city = message_city()[0]
    if city in all_city:
        UsersFiltersBd().update_filters_user(id_vk=id_vk, city_id=city, city_title=all_city[city])
        return 'Город установлен'
    else:
        return 'Такой город недоступен'


def marks_person(id_vk: int) -> str:
    """Функция вычисляет, сколько людей отметило пользователя с id_vk"""
    mark_person = len(LikedListBD().get_all_marks_user(id_vk))
    message = choose_plural(mark_person, ('человек', 'человека', 'человек'))
    return f"{message[0]} {message[1]}"


def get_message_search(id_vk: int) -> dict:
    """
    Достает из SearchPeople первую попавшуюся запись, которая связана с записью из Users.
    Формирует выходное сообщение из информации, получаемой с методов get_user_vk и get_photo_user
    """
    session = session_bd(PATH)
    session = session()

    user = (session.query(Users.id_vk, SearchPeople.id_user)
            .filter_by(id_vk=id_vk)
            .join(SearchPeople, SearchPeople.id_user_main == Users.id_vk).first())
    search = SearchVK(VK_KEY_API)
    user_info = search.get_user_vk(user[1])
    attachment = get_id_vk_users_photo(user_info['id_user'])
    return {
        'message': f"Имя: {user_info['first_name']} {user_info['last_name']}\n"
                   f"Возраст: {calculate_age(user_info['bdate'])}\n"
                   f"Город: {user_info['city_title']}\n"
                   f"{'Профиль скрыт, есть только главная фотография по ссылке на профиль' if not attachment else ''}",
        'attachment': ','.join(attachment) if attachment else None,
        'id_user': user_info['id_user'],
        'url_profile': 'https://vk.com/id' + str(user[1])
    }


def save_search_people(id_user: int, check: bool = False) -> None:
    """
    Функция проверяет, если ли в таблице SearchPeople записи с id_user,
    если нет ни одной записи, то функция записывает людей в SearchPeople.
    При check == True, функция перезапишет имеющиеся данные
    """
    search_people = SearchPeopleBd()
    user = search_people.get_user(id_user)
    if user is None or check:
        if check:
            search_people.delete_user_all(id_user)
        peoples = SearchVK(VK_KEY_API)
        filters = UsersFiltersBd()
        get_f = filters.get_filters_user(id_user)
        users_id = [user['id'] for user in peoples.get_users_vk(1000,
                                                                sex=get_f.sex,
                                                                age_from=get_f.age_from,
                                                                age_to=get_f.age_to,
                                                                city_id=get_f.city_id,
                                                                city_title=get_f.city_title,
                                                                relation=get_f.relation,
                                                                is_closed=False) if not user['is_closed']]
        shuffle(users_id)
        SearchPeopleBd().add_users(id_user_main=id_user, id_users=users_id)


def get_id_vk_users_photo(id_user: int) -> list[str]:
    """
    Функция достает из профиля все фотографии пользователя и составляет из них id в формате photo<id_user>_<id_photo>
    """
    search = SearchVK(VK_KEY_API)
    user_photo = search.get_photo_user(id_user, max_count=3)
    if not isinstance(user_photo, int) and len(user_photo) < 3:
        user_photo = {**search.get_photo_user(id_user, max_count=3 - len(user_photo), place='wall'), **user_photo}
    if not isinstance(user_photo, int):
        attachment = ['photo{}_{}'.format(id_user, id_photo) for id_photo in list(user_photo)[::-1]]
    else:
        attachment = None

    return attachment
