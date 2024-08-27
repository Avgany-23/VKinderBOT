from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_bot.menu_button import *
from vk_bot.bot_function import *
from vk_bot.utils import decorator_check_users_or_create_him
from database.crud_db.search_people import SearchPeopleBd
from settings import TOKEN_BOT, GROUP_ID_VK
import json
import re


vk = VkApi(token=TOKEN_BOT)
vk_ = vk.get_api()
long_poll = VkBotLongPoll(vk, GROUP_ID_VK)


for event in long_poll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:                                # Событие на получение сообщения
        if event.from_user:
            message = event.obj.message
            id_user = event.obj.message['from_id']
            request = message['text'].lower()
            pay_load_type = json.loads(message['payload'])['type'] if 'payload' in message else ''

            if pay_load_type == 'search_people':                                # Кнопка "Найти половинку"
                save_search_people(id_user)
                info_user = get_message_search(id_user)
                send_message(vk=vk, user_id=id_user, message=info_user['message'],
                             attachment=info_user['attachment'], keyboard=search_inline())
                SearchPeopleBd().delete_user(id_user, info_user['id_user'])
            elif pay_load_type in ('Like list', 'Block list'):                  # Кнопка "Найти половинку"
                send_message(vk, id_user, list_users(id_user, count=15, list_user=request))
            elif pay_load_type == 'next_people':                                # Кнопка "Следующий человек"
                ...
            elif pay_load_type == 'browsing_history':                           # Кнопка "История просмотров"
                send_message(vk, id_user, browsing_history(15))
            elif pay_load_type == 'filters':                                    # Кнопка "Фильтры поиска людей"
                decorator_check_users_or_create_him(id_user)(send_message)(vk=vk,
                                                                           user_id=id_user,
                                                                           message=user_filters(id_user),
                                                                           keyboard=filters_menu())
            elif pay_load_type[:7] == 'filter_':
                pay_load_type = pay_load_type[7:]
                if re.findall(r'(\d{2}-\d{2})|>35', pay_load_type):  # Обнова age
                    change_filter_age(id_user, request), send_message(vk, id_user, 'Возраст установлен')
                elif pay_load_type in ('sex-male', 'sex-female'):                   # Inline кнопка установки пола
                    change_filter_sex(id_user, request), send_message(vk, id_user, 'Пол установлен')
                save_search_people(id_user, check=True)
            elif re.findall(r'Установить возраст:?[ ]?\d{1,}[- ]\d{1,}', request, re.IGNORECASE):
                change_filter_age(id_user, request), send_message(vk, id_user, 'Возраст установлен')
                save_search_people(id_user, check=True)
            elif request == "меню":                                             # Сообщение "Меню" - пока что её нет
                send_message(vk, id_user, 'Главное меню', main_menu(id_user))
            else:                                                               # Остальные сообщения
                send_message(vk, id_user, 'Чее ??')

    if event.type == VkBotEventType.MESSAGE_EVENT:      # Событие на нажатие кнопки
        callback = event.object.payload.get('type')     # действие callback
        id_user = event.object.user_id                  # id пользователя


        if callback == 'show_snackbar':                 # Кнопка "Ваши отметки"
            snow_snackbar(vk, event.object.event_id, id_user, event.object.peer_id, json.dumps(event.object.payload))
            if event.object['payload']['text'].find('черный список') > 0:
                ...
        if callback == 'main_menu':
            send_message(vk, id_user, 'Главное меню', main_menu(id_user))
        if callback == 'next_people':
            save_search_people(id_user)
            info_user = get_message_search(id_user)
            last_id = vk_.messages.edit(
                peer_id=event.obj.peer_id,
                message=info_user['message'],
                conversation_message_id=event.obj.conversation_message_id,
                attachment=info_user['attachment'],
                keyboard=search_inline().get_keyboard()
            )
            SearchPeopleBd().delete_user(id_user, info_user['id_user'])















# from vk_api import VkApi
# from vk_api.utils import get_random_id
# from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
# from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# import json
# from dotenv import load_dotenv
# import os
# from vk_bot.bot_function import *
#
#
# load_dotenv()
#
#
# vk_session = VkApi(token=os.getenv('token_bot'))
# # vk_session = VkApi(token=os.getenv('token_bot'), api_version='5.120')
# vk = vk_session.get_api()
# longpoll = VkBotLongPoll(vk_session, 227063965)
#
# CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
#
# settings = dict(one_time=False, inline=True)
#
# # №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
# keyboard_1 = VkKeyboard(**settings)
# # pop-up кнопка
# keyboard_1.add_callback_button(label='Покажи pop-up сообщение', color=VkKeyboardColor.SECONDARY, payload={"type": "show_snackbar", "text": "Это исчезающее сообщение"})
# keyboard_1.add_line()
# # кнопка с URL
# keyboard_1.add_callback_button(label='Откртыть Url', color=VkKeyboardColor.POSITIVE, payload={"type": "open_link", "link": "https://vk.com/dev/bots_docs_5"})
# keyboard_1.add_line()
# # кнопка переключения на 2ое меню
# keyboard_1.add_callback_button(label='Добавить красного ', color=VkKeyboardColor.PRIMARY, payload={"type": "my_own_100500_type_edit"})
#
# # №2. Клавиатура с одной красной callback-кнопкой. Нажатие изменяет меню на предыдущее.
# keyboard_2 = VkKeyboard(**settings)
# # кнопка переключения назад, на 1ое меню.
# keyboard_2.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE, payload={"type": "my_own_100500_type_edit"})
#
# f_toggle: bool = False
# for event in longpoll.listen():
#     # отправляем меню 1го вида на любое текстовое сообщение от пользователя
#     if event.type == VkBotEventType.MESSAGE_NEW:
#         if event.obj.message['text']:
#             if event.from_user:
#
#                 if 'callback' not in event.obj.client_info['button_actions']:
#                     print(f'Клиент {event.obj.message["from_id"]} не поддерж. callback')
#
#                 send_message(vk_session, event.obj.message['from_id'], 'Ну привет', keyboard_1)
#                 # vk.messages.send(
#                 #         user_id=event.obj.message['from_id'],
#                 #         random_id=get_random_id(),
#                 #         peer_id=event.obj.message['from_id'],
#                 #         keyboard=keyboard_1.get_keyboard(),
#                 #         message=event.obj.message['text'])
#                 # send_message(vk, event.obj.message['from_id'], 'удачи', keyboard=keyboard_1)
#     # обрабатываем клики по callback кнопкам
#     elif event.type == VkBotEventType.MESSAGE_EVENT:
#
#         if event.object.payload.get('type') in CALLBACK_TYPES:
#             r = vk.messages.sendMessageEventAnswer(
#                       event_id=event.object.event_id,
#                       user_id=event.object.user_id,
#                       peer_id=event.object.peer_id,
#                       event_data=json.dumps(event.object.payload))
#         elif event.object.payload.get('type') == 'my_own_100500_type_edit':
#             # send_message(vk, event.obj.message['from_id'], 'удачи')
#             print(event.obj.peer_id)
#             print(event.obj.conversation_message_id)
#             last_id = vk.messages.edit(
#                       peer_id=event.obj.peer_id,
#                       message='ola',
#                       conversation_message_id=event.obj.conversation_message_id,
#                       keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard())
#             f_toggle = not f_toggle