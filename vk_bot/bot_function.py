from vk_api import VkApi, VkUpload, vk_api
from vk_api.utils import get_random_id
from typing import Optional
from vk_api.keyboard import VkKeyboard
from PIL import Image
import json


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


def list_users(count: int = 15, list_user: str = 'liked') -> str:
    """
    Возвращает count пользователей из БД.
    list_user: like_pages - из таблицы LikedList, block_pages - из таблицы BlackList
    """
    if list_user == 'Like list':
        return 'Список отмеченных пользователей: %s' % count
    return 'Список игнорируемых пользователей: %s' % count


def browsing_history(count):
    """Из таблицы с историей просмотров достает последние count записей"""
    return 'Ваша история просмотров: %s' % count


def user_filters(id_user):
    """Возвращает описание пользовательских фильтров"""
    return f'Фильтры поиска:\n{id_user}'


def get_photo_vk_id(path: str, vk: vk_api.VkApi) -> str:
    """Получение vk-id фотографий"""
    upload = VkUpload(vk)
    upload_img = upload.photo_messages(photos=path)[0]
    return '{}_{}'.format(upload_img['owner_id'], upload_img['id'])


def correct_size_photo(path: str, width: int = 1300, height: int = 800) -> None:
    """Изменение соотношение сторон, по умолчанию 13 к 8"""
    with Image.open(path) as photo:
        result = photo.resize((width, height))
        result.save(path)


def carousel_str(photo_id: list, label: str = 'Поставить лайк') -> str:
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


def get_template_carousel(vk, path) -> str:
    result_photos = []
    for el in path:
        correct_size_photo(el)
        result_photos.append(get_photo_vk_id(el, vk))

    return carousel_str(result_photos)