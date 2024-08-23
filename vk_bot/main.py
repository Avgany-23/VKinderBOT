from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkApi
from typing import Optional


def send_message(vk: VkApi, user_id: int, message: str, keyboard: Optional[VkKeyboard] = None) -> None:
    """Отправка сообщения ботом в чат"""
    values = {
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id()
    }

    if keyboard:
        values['keyboard'] = keyboard.get_keyboard()

    vk.method('messages.send', values)


def inline_main_menu() -> VkKeyboard:
    """Inline клавиатура главного меню"""
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button('Кнопка1', color=VkKeyboardColor.PRIMARY, payload={"type": "my_own_100500_type_edit"})
    keyboard.add_callback_button('Кнопка2', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_callback_button('Кнопка3', color=VkKeyboardColor.PRIMARY)
    keyboard.add_callback_button('Добавить красного ', color=VkKeyboardColor.PRIMARY,
                                   payload={"type": "my_own_100500_type_edit"})

    return keyboard
