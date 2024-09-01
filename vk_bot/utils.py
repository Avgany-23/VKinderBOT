from database.crud_db.filters_users import UsersFiltersBd
from database.crud_db.info_users import InfoUsersBd
from database.crud_db.users import UsersBd
from api_vk.main import SearchVK
from settings import VK_KEY_API
from datetime import datetime
from functools import wraps


def decorator_check_users_or_create_him(id_vk: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            create_user = UsersBd().create_user(id_vk)
            if create_user:  # Если пользователь создался, значит надо инициализировать его в InfoUsers и FiltersUsers
                from logs.logs import logger_base

                vk_user = SearchVK(VK_KEY_API)
                user_info = vk_user.get_user_vk(id_vk)
                result_create_user = InfoUsersBd().add_info_users(**user_info)
                if result_create_user == 1:
                    logger_base.info(f'Пользователь с vk_id = {id_vk} успешно создался')
                else:
                    logger_base.error(f'Пользователь с vk_id = {id_vk} не создался. Проверьте '
                                      f'InfoUsersBd().add_info_users')
                UsersFiltersBd().add_filters_users(**format_for_filters_users(user_info))

            return func(*args, **kwargs)
        return wrapper
    return decorator


def choose_plural(amount: int, declensions: tuple[str, str, str]) -> tuple[int, str]:
    """
    Функция для склонения слов. Принимает число и 3 варианта его склонения,
    Например, 91 ('день', 'дня', 'дней')
    Принимает amount - количество (int), declensions - список склонений (кортеж строк)
    Возвращает строку, содержащую в себе число и правильное склонение
    """
    selector = {
        amount % 10 == 1: 0,
        amount % 10 in [2, 3, 4]: 1,
        amount % 10 in [0, 5, 6, 7, 8, 9]: 2,
        amount % 100 in range(11, 21): 2
    }
    return amount, declensions[selector[True]]


def calculate_age(date_: str) -> int | str:
    """Определяет возраст человека (в годах). Принимает дату в формате d.m.y"""
    try:
        birthday = datetime.strptime(date_, '%d.%m.%Y')
    except ValueError:
        return 'возраст не определён'
    today = datetime.now()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def filter_age(birth_date: str, end_range: int = 5) -> tuple[int, int]:
    """Вычисляет диапазон от количества лет с даты birth_date и значения end_range"""
    age = calculate_age(birth_date)
    if age > 35:
        return 35, 100
    return age, age + end_range


def format_for_filters_users(info: dict[str: str]) -> dict[str: str]:
    """Берёт из словаря info только те значения, которые находятся в модели FiltersUsers"""
    info['sex'] = 1 if info['sex'] == 2 else 2
    range_age = filter_age(info['bdate'])
    return {'id_user': info['id_user'], 'sex': info['sex'], 'age_from': range_age[0], 'age_to': range_age[1],
            'city_id': info['city_id'], 'city_title': info['city_title'], 'relation': info['relation']}


def message_status() -> tuple[dict[int, str], str]:
    dict_status = {
        0: 'статус не важен',
        1: 'не женат (не замужем)',
        2: 'встречается',
        3: 'помолвлен(-а)',
        4: 'женат (замужем)',
        5: 'всё сложно',
        6: 'в активном поиске',
        7: 'влюблен(-а)',
        8: 'в гражданском браке',
    }

    return dict_status, ('Доступны следующие статусы:\n'
                         '0 - статус не важен\n'
                         '1 - не женат (не замужем)\n'
                         '2 - встречается\n'
                         '3 - помолвлен(-а)\n'
                         '4 - женат (замужем)\n'
                         '5 - всё сложно\n'
                         '6 - в активном поиске\n'
                         '7 - влюблен(-а)\n'
                         '8 - в гражданском браке\n\n'
                         'Для установки статуса введите сообщение в формате:\n'
                         'статус n\n-- где n - номер статуса из списка')


def message_city() -> tuple[dict[int, str], str]:
    dict_city = {
        0: 'Любой',
        1: 'Москва',
        2: 'Санкт-Петербург',
        37: 'Владивосток',
        42: 'Воронеж',
        60: 'Казань',
        73: 'Красноярск',
        158: 'Челябинск',

    }
    return dict_city, ('Доступны следующие города:\n'
                       '0 - Любой\n'
                       '1 - Москва\n'
                       '2 - Санкт-Петербург\n'
                       '37 - Владивосток\n'
                       '42 - Воронеж\n'
                       '60 - Казань\n'
                       '73 - Красноярск\n'
                       '158 - Челябинск\n\n'
                       'Для установки города введите сообщение в формате:\n'
                       'город n\n-- где n - номер города из списка')
