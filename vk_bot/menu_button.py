from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_bot.bot_function import marks_person, redis_get_prev_person, redis_person_is_current, redis_person_is_last
from database import session_bd, PATH
from database.models import Users, LikedList, BlackList
from sqlalchemy import join


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
                        payload={"type": "filter_14-18"})
    keyboard.add_button('19-25',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_19-25"})
    keyboard.add_button('26-35',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_26-35"})
    keyboard.add_button('>35',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_>35"})
    keyboard.add_line()
    keyboard.add_callback_button('Пол:',
                                 color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_snackbar", "text": "Выбор пола"})
    keyboard.add_button('мужской',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_sex-male"})
    keyboard.add_button('женский',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_sex-female"})
    return keyboard


def search_inline(url_profile: str, id_vk: int, user_list_id: int, prev_none: bool = False) -> VkKeyboard:
    """Список отмеченных/заблокированных пользователей"""
    keyboard = VkKeyboard(one_time=False, inline=True)
    info_user = redis_person_is_last(id_vk)    # Информация для определения кнопки prev_people
    # print(info_user)
    if prev_none or redis_person_is_last(id_vk):
        keyboard.add_callback_button('Предыдущей записи нет',
                                     color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "show_snackbar",
                                              "text": "Нельзя вернуться на предыдущую запись"})
    else:
        keyboard.add_callback_button('⬅Предыдущий человек',
                                     color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "prev_people"})
    keyboard.add_callback_button('➡️Следующий человек',
                                 color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "next_people"})
    keyboard.add_line()

    # --- Проверка на наличие человека в списке Избранного/ЧС для выбора подходящей кнопки ---
    session = session_bd(PATH)
    with (session() as sess):
        check_lists_result = (sess.query(Users.id_vk, LikedList.id_like_user, BlackList.id_ignore_user).
                              join(BlackList, Users.id_vk == BlackList.id_user).
                              outerjoin(LikedList, Users.id_vk == LikedList.id_user).
                              filter(Users.id_vk == id_vk)).all()
        button_liked_list = True
        button_black_list = True
        if check_lists_result:
            button_liked_list = not any(user_list_id == id_[1] for id_ in check_lists_result)
            button_black_list = not any(user_list_id == id_[2] for id_ in check_lists_result)

    if button_black_list:
        keyboard.add_callback_button('❌Больше не показывать',
                                     color=VkKeyboardColor.NEGATIVE,
                                     payload={"type": "show_snackbar",
                                              "text": "Пользователь добавлен в черный список"})
    else:
        keyboard.add_callback_button('❌Убрать из игнорируемых',
                                     color=VkKeyboardColor.NEGATIVE,
                                     payload={"type": "show_snackbar",
                                              "text": "Пользователь удален из черного списка"})

    if button_liked_list:
        keyboard.add_callback_button('💛Сохранить в список',
                                     color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "show_snackbar",
                                              "text": "Пользователь добавлен в список избранного"})
    else:
        keyboard.add_callback_button('💛Удалить из списка',
                                     color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "show_snackbar",
                                              "text": "Пользователь удален из списка избранного"})
    keyboard.add_line()
    keyboard.add_callback_button('Ссылка на профиль',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "open_link",
                                          'link': url_profile})
    return keyboard


def search_menu():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button('Ссылка 1',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "open_link",
                                          'link': 'https://vk-api.readthedocs.io/en/latest/bot_longpoll.html'})
    keyboard.add_line()
    keyboard.add_callback_button('Ссылка 2',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "open_link",
                                          'link': 'https://vk-api.readthedocs.io/en/latest/bot_longpoll.html'})
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
