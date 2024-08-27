from datetime import datetime
from vk_api import VkUpload, vk_api
from PIL import Image
from functools import wraps
from database.crud_db.users import UsersBd
from database.crud_db.info_users import InfoUsersBd
from database.crud_db.filters_users import UsersFiltersBd
from api_vk.main import SearchVK
from settings import VK_KEY_API
import json


def decorator_check_users_or_create_him(id_vk: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            create_user = UsersBd().create_user(id_vk)
            if create_user:  # Если пользователь создался, значит надо инициализировать его в InfoUsers и FiltersUsers
                vk_user = SearchVK(VK_KEY_API)
                user_info = vk_user.get_user_vk(id_vk)
                InfoUsersBd().add_info_users(**user_info)
                UsersFiltersBd().add_filters_users(**format_for_filters_users(user_info))
            return func(*args, **kwargs)
        return wrapper
    return decorator


# def decorator_find_user_search(id_user: int):
#     """"""
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             save_search_people(id_user)
#             info_user = get_message_search(id_user)
#             result = func(*args, **kwargs)
#
#             return result
#         return wrapper
#     return decorator


def correct_size_photo(path: str, width: int = 1300, height: int = 800) -> None:
    """Изменение соотношение сторон, по умолчанию 13 к 8"""
    with Image.open(path) as photo:
        result = photo.resize((width, height))
        result.save(path)


def choose_plural(amount: int, declensions: tuple[str, str, str]) -> tuple[int, str]:
    """Функция для склонения слов. Принимает число и 3 варианта его склонения,
    Например, 91 ('день', 'дня', 'дней')
    Принимает amount - количество (int), declensions - список склонений (кортеж строк)
    Возвращает строку, содержащую в себе число и правильное склонение"""
    selector = {
        amount % 10 == 1: 0,
        amount % 10 in [2, 3, 4]: 1,
        amount % 10 in [0, 5, 6, 7, 8, 9]: 2,
        amount % 100 in range(11, 21): 2
    }
    return amount, declensions[selector[True]]


def get_photo_vk_id(path: str, vk: vk_api.VkApi) -> str:
    """Получение vk-id фотографий"""
    upload = VkUpload(vk)
    upload_img = upload.photo_messages(photos=path)[0]
    return '{}_{}'.format(upload_img['owner_id'], upload_img['id'])


def carousel_str(photo_id: list, label: str = 'Поставить лайк') -> str:
    """Получение json карусели для VK-бота"""
    carousel_ = {"type": "carousel", "elements": []}
    for photo in photo_id:
        element = {
            "photo_id": photo,
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": label,
                    "payload": "{}"
                }
            }]
        }
        carousel_['elements'].append(element)
    result = json.dumps(carousel_)

    return result


def calculate_age(date_: str) -> int:
    """Определяет возраст человека (в годах)"""
    birthday = datetime.strptime(date_, '%d.%m.%Y')
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
    return {'id_user': info['id_user'], 'sex': info['sex'], 'age_from': range_age[0], 'age_to': range_age[1], 'city_id': info['city_id'],
            'city_title': info['city_title'], 'relation': info['relation']}
