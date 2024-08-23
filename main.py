# from vk_api.longpoll import VkLongPoll, VkEventType
# from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
# from vk_bot.main import *
# from vk_bot.bot_function import *
#
# from dotenv import load_dotenv
# import os
#
#
# load_dotenv()
#
#
# vk = vk_api.VkApi(token=os.getenv('token_bot'))
# long_poll = VkLongPoll(vk)
#
#
# for event in long_poll.listen():
#     if event.type == VkBotEventType.MESSAGE_EVENT:  # Событие на нажатие кнопки
#         print(event.type)
#         # if event.from_user:
#         #     print(event.payload)  # Выводим payload кнопки
#         #     if event.payload == ['кнопка1']:  # Проверяем payload кнопки
#         #         send_message(vk, id_user, 'удачи')
#
#
#     if event.type == VkEventType.MESSAGE_NEW:   # Событие на получение сообщения
#         if event.to_me:
#             print(111)
#             id_user = event.user_id
#             request = event.text
#
#             if request == "привет":
#                 send_message(vk, id_user, 'Ну привет')
#             elif request == "пока":
#                 send_message(vk, id_user, 'Ну пока', inline_main_menu())
#             else:
#                 send_message(vk, id_user, 'Чее ??')
















from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
from dotenv import load_dotenv
import os
from vk_bot.main import *
from vk_bot.bot_function import *


load_dotenv()


vk_session = VkApi(token=os.getenv('token_bot'))
# vk_session = VkApi(token=os.getenv('token_bot'), api_version='5.120')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 227063965)

CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')

settings = dict(one_time=False, inline=True)

# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**settings)
# pop-up кнопка
keyboard_1.add_callback_button(label='Покажи pop-up сообщение', color=VkKeyboardColor.SECONDARY, payload={"type": "show_snackbar", "text": "Это исчезающее сообщение"})
keyboard_1.add_line()
# кнопка с URL
keyboard_1.add_callback_button(label='Откртыть Url', color=VkKeyboardColor.POSITIVE, payload={"type": "open_link", "link": "https://vk.com/dev/bots_docs_5"})
keyboard_1.add_line()
# кнопка переключения на 2ое меню
keyboard_1.add_callback_button(label='Добавить красного ', color=VkKeyboardColor.PRIMARY, payload={"type": "my_own_100500_type_edit"})

# №2. Клавиатура с одной красной callback-кнопкой. Нажатие изменяет меню на предыдущее.
keyboard_2 = VkKeyboard(**settings)
# кнопка переключения назад, на 1ое меню.
keyboard_2.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE, payload={"type": "my_own_100500_type_edit"})

f_toggle: bool = False
for event in longpoll.listen():
    # отправляем меню 1го вида на любое текстовое сообщение от пользователя
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.message['text'] != '':
            if event.from_user:
                # Если клиент пользователя не поддерживает callback-кнопки,
                # нажатие на них будет отправлять текстовые
                # сообщения. Т.е. они будут работать как обычные inline кнопки.
                if 'callback' not in event.obj.client_info['button_actions']:
                    print(f'Клиент {event.obj.message["from_id"]} не поддерж. callback')

                vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=keyboard_1.get_keyboard(),
                        message=event.obj.message['text'])
                # send_message(vk, event.obj.message['from_id'], 'удачи', keyboard=keyboard_1)
    # обрабатываем клики по callback кнопкам
    elif event.type == VkBotEventType.MESSAGE_EVENT:

        # если это одно из 3х встроенных действий:
        if event.object.payload.get('type') in CALLBACK_TYPES:
            # отправляем серверу указания как какую из кнопок обработать. Это заложено в
            # payload каждой callback-кнопки при ее создании.
            # Но можно сделать иначе: в payload положить свои собственные
            # идентификаторы кнопок, а здесь по ним определить
            # какой запрос надо послать. Реализован первый вариант.
            # send_message(vk, event.obj.message['from_id'], 'удачи')
            r = vk.messages.sendMessageEventAnswer(
                      event_id=event.object.event_id,
                      user_id=event.object.user_id,
                      peer_id=event.object.peer_id,
                      event_data=json.dumps(event.object.payload))
        # если это наша "кастомная" (т.е. без встроенного действия) кнопка, то мы можем
        # выполнить edit сообщения и изменить его меню. Но при желании мы могли бы
        # на этот клик открыть ссылку/приложение или показать pop-up. (см.анимацию ниже)
        elif event.object.payload.get('type') == 'my_own_100500_type_edit':
            # send_message(vk, event.obj.message['from_id'], 'удачи')
            last_id = vk.messages.edit(
                      peer_id=event.obj.peer_id,
                      message='ola',
                      conversation_message_id=event.obj.conversation_message_id,
                      keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard())
            # f_toggle = not f_toggle