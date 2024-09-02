from database.requests_redis import redis_person_is_last
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from database.models import Users, LikedList, BlackList
from vk_bot.bot_function import marks_person
from database import session_bd, PATH


def main_menu(id_vk) -> VkKeyboard:
    """Клавиатура главного меню"""
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Найти половинку 💙',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "search_people"})
    keyboard.add_line()
    keyboard.add_button(label='Фильтры поиска людей',
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": "filters"})
    keyboard.add_line()
    keyboard.add_button(label='Like list',
                        color=VkKeyboardColor.POSITIVE,
                        payload={"type": "Like list"})
    keyboard.add_button(label='Block list',
                        color=VkKeyboardColor.NEGATIVE,
                        payload={"type": "Block list"})
    keyboard.add_line()
    keyboard.add_button(label='История просмотров',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "browsing_history"})
    keyboard.add_callback_button(label='Ваши отметки',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "show_snackbar",
                                          "text": f"Вас отметило {marks_person(id_vk)}, вы никому не нужны"})

    return keyboard


def filters_menu() -> VkKeyboard:
    """Меню с выбором фильтров поиска"""
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label='Возраст:',
                                 color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_snackbar", "text": "Выбор возраста"})
    keyboard.add_button(label='14-18',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_14-18"})
    keyboard.add_button(label='19-25',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_19-25"})
    keyboard.add_button(label='26-35',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_26-35"})
    keyboard.add_button(label='>35',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_>35"})
    keyboard.add_line()
    keyboard.add_callback_button(label='Пол:',
                                 color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_snackbar", "text": "Выбор пола"})
    keyboard.add_button(label='мужской',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_sex-male"})
    keyboard.add_button(label='женский',
                        color=VkKeyboardColor.SECONDARY,
                        payload={"type": "filter_sex-female"})
    keyboard.add_line()
    keyboard.add_button(label='Статус: нажать для получения информации',
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": "info_status"})
    keyboard.add_line()
    keyboard.add_button(label='Город: нажать для получения информации',
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": "info_city"})
    return keyboard


def search_inline(url_profile: str, id_vk: int, user_list_id: int, prev_none: bool = False) -> VkKeyboard:
    """Список отмеченных/заблокированных пользователей"""
    keyboard = VkKeyboard(one_time=False, inline=True)

    if prev_none or redis_person_is_last(id_vk):
        keyboard.add_callback_button(label='Предыдущей записи нет',
                                     color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "show_snackbar",
                                              "text": "Нельзя вернуться на предыдущую запись"})
    else:
        keyboard.add_callback_button(label='⬅Предыдущий человек',
                                     color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "prev_people"})
    keyboard.add_callback_button(label='➡️Следующий человек',
                                 color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "next_people"})
    keyboard.add_line()

    # --- Проверка на наличие человека в списке Избранного/ЧС для выбора подходящей кнопки ---
    session = session_bd(PATH)
    with session() as sess:
        from sqlalchemy import and_
        check_lists_result = (sess.query(Users.id_vk,
                                         LikedList.id_like_user,
                                         BlackList.id_ignore_user,
                                         LikedList.name_user,
                                         BlackList.name_user).
                              outerjoin(LikedList, and_(Users.id_vk == LikedList.id_user,
                                                        LikedList.id_like_user == user_list_id)).
                              outerjoin(BlackList, and_(Users.id_vk == BlackList.id_user,
                                                        BlackList.id_ignore_user == user_list_id)).
                              filter(Users.id_vk == id_vk)).all()[0]

        # Если True, значит кнопка "Больше не показывать", False - "Убрать из игнорируемых"
        button_liked_list = check_lists_result[1] is None
        # Если True, значит кнопка "Сохранить в список", False - "Удалить из списка"
        button_black_list = check_lists_result[2] is None

    if button_black_list:
        keyboard.add_callback_button(label='❌Больше не показывать',
                                     color=VkKeyboardColor.NEGATIVE,
                                     payload={"type": "show_snackbar",
                                              "text": f"Пользователь добавлен в черный список"})
    else:
        keyboard.add_callback_button(label='❌Убрать из игнорируемых',
                                     color=VkKeyboardColor.NEGATIVE,
                                     payload={"type": "show_snackbar",
                                              "text": f"Пользователь удален из черного списка"})

    if button_liked_list:
        keyboard.add_callback_button(label='💛Сохранить в список',
                                     color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "show_snackbar",
                                              "text": f"Пользователь добавлен в список избранного"})
    else:
        keyboard.add_callback_button(label='💛Удалить из списка',
                                     color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "show_snackbar",
                                              "text": f"Пользователь удален из списка избранного"})
    keyboard.add_line()
    keyboard.add_callback_button(label='Ссылка на профиль',
                                 color=VkKeyboardColor.SECONDARY,
                                 payload={"type": "open_link",
                                          'link': url_profile})
    return keyboard


def like_block_list(people: str) -> VkKeyboard:
    """Кнопка для очистки списка"""
    text = 'список избранного' if people == 'Like list' else 'черный список'
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label='Очистить список',
                                 color=VkKeyboardColor.NEGATIVE,
                                 payload={"type": "show_snackbar",
                                          "text": text + ' очищен'})
    return keyboard
