from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_function import marks_person


def main_menu(id_vk) -> VkKeyboard:
    """Inline клавиатура главного меню"""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Найти половинку 💙',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "search_people"})
    keyboard.add_line()
    keyboard.add_button('Фильтры поиска людей',
                                 color=VkKeyboardColor.PRIMARY,
                                 payload={"type": "filters"})
    keyboard.add_line()
    keyboard.add_button('Like list',
                        color=VkKeyboardColor.POSITIVE,
                        payload={"type": "Like list"})
    keyboard.add_button('Block list',
                        color=VkKeyboardColor.NEGATIVE,
                        payload={"type": "Block list"})
    keyboard.add_line()
    keyboard.add_button('История просмотров',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "browsing_history"})
    keyboard.add_callback_button('Ваши отметки',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "show_snackbar",
                                          "text": f"Вас отметило {marks_person(id_vk)}, вы никому не нужны"})

    return keyboard


def filters_menu() -> VkKeyboard:
    """Меню с выбором фильтров поиска"""
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button('Настройка фильтров, выберите параметры:',
                                 color=VkKeyboardColor.PRIMARY,
                                 payload={"type": "show_snackbar", "text": "Выберите настройки фильтров"})
    keyboard.add_line()
    keyboard.add_callback_button('Возраст:',
                                 color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_snackbar", "text": "Выбор возраста"})
    keyboard.add_button('14-18',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "14-18"})
    keyboard.add_button('19-25',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "19-25"})
    keyboard.add_button('26-35',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "26-35"})
    keyboard.add_button('>35',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": ">35"})
    keyboard.add_line()
    keyboard.add_callback_button('Пол:',
                                 color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_snackbar", "text": "Выбор пола"})
    keyboard.add_button('мужской',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "sex-male"})
    keyboard.add_button('женский',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "sex-female"})
    return keyboard


# def like_or_block_menu() -> VkKeyboard:
#     """Список отмеченных/заблокированных пользователей"""
#     keyboard = VkKeyboard(one_time=False, inline=True)
#     keyboard.add_callback_button('Тут будут фильтры',
#                                  color=VkKeyboardColor.SECONDARY,
#                                  payload={"type": "search_people"})
#     keyboard.add_line()
#     keyboard.add_button('Вернуться назад',
#                                  color=VkKeyboardColor.SECONDARY,
#                                  payload={"type": "main_menu"})
#     return keyboard


def search_menu():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button('Ссылка 1',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "open_link", 'link': 'https://vk-api.readthedocs.io/en/latest/bot_longpoll.html'})
    keyboard.add_line()
    keyboard.add_callback_button('Ссылка 2',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "open_link", 'link': 'https://vk-api.readthedocs.io/en/latest/bot_longpoll.html'})
    return keyboard


# def inline_main_menu() -> VkKeyboard:
#     """Inline клавиатура главного меню"""
#     keyboard = VkKeyboard(one_time=False, inline=True)
#     keyboard.add_callback_button('Кнопка1', color=VkKeyboardColor.PRIMARY, payload={"type": "my_own_100500_type_edit"})
#     keyboard.add_callback_button('Кнопка2', color=VkKeyboardColor.NEGATIVE, payload={"type": "open_link", "link": "https://vk.com/dev/bots_docs_5"})
#     keyboard.add_callback_button('Кнопка3', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": "https://vk.com/dev/bots_docs_5"})
#     keyboard.add_callback_button('Добавить красного ', color=VkKeyboardColor.PRIMARY,
#                                    payload={"type": "my_own_100500_type_edit"})
#
#     return keyboard