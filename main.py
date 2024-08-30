from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_bot.utils import decorator_check_users_or_create_him
from settings import TOKEN_BOT, GROUP_ID_VK, HISTORY_SIZE
from vk_bot.menu_button import *
from vk_bot.bot_function import *
from database.requests_redis import *
import json
import re


vk = VkApi(token=TOKEN_BOT)
vk_ = vk.get_api()
long_poll = VkBotLongPoll(vk, GROUP_ID_VK)


for event in long_poll.listen():

    # Событие на получение сообщения
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_user:
            message = event.obj.message
            id_user = event.obj.message['from_id']
            request = message['text'].lower()
            pay_load_type = json.loads(message['payload'])['type'] if 'payload' in message else ''

            # ------ Кнопка "Найти половинку" ------
            if pay_load_type == 'search_people':
                redis_clear_user_id(id_user)                                    # Очистка прежнего кеша пользователя
                decorator_check_users_or_create_him(id_user)(save_search_people)(id_user)
                info_user = get_message_search(id_user)
                redis_set_person(id_user, info_user)
                redis_set_current_person(id_user, info_user['id_user'])
                redis_save_history(id_user, info_user, size=HISTORY_SIZE)    # Сохранение в историю анкет Redis
                SearchPeopleBd().delete_user(id_user, info_user['id_user'])  # Удаление прошлой записи
                send_message(vk=vk, user_id=id_user,
                             message=info_user['message'],
                             attachment=info_user['attachment'],
                             keyboard=search_inline(info_user['url_profile'], id_user, info_user['id_user']))

            # ------ Кнопка "Like List" и "BLock list" ------
            elif pay_load_type in ('Like list', 'Block list'):
                message = list_users(id_user, list_user=request)
                send_message(vk=vk,
                             user_id=id_user,
                             message=message,
                             keyboard=None if message == 'Список пуст' else like_block_list(pay_load_type))

            # ------ Кнопка "История просмотров" ------
            elif pay_load_type == 'browsing_history':
                send_message(vk, id_user, redis_browsing_history(id_user))

            # ------ Кнопка "Фильтры поиска людей" - вывод текущих фильтров и их настроек ------
            elif pay_load_type == 'filters':
                send_message(vk=vk,
                             user_id=id_user,
                             message=decorator_check_users_or_create_him(id_user)(user_filters)(id_user),
                             keyboard=filters_menu())

            # ------ Кнопка с обновлением возраста и пола ------
            elif pay_load_type[:7] == 'filter_':
                pay_load_type = pay_load_type[7:]
                if re.findall(r'(\d{2}-\d{2})|>35', pay_load_type):         # Обновление возраста
                    change_filter_age(id_user, request), send_message(vk, id_user, 'Возраст установлен')
                elif pay_load_type in ('sex-male', 'sex-female'):                   # Inline кнопка установки пола
                    change_filter_sex(id_user, request), send_message(vk, id_user, 'Пол установлен')
                save_search_people(id_user, check=True)

            # ------ Сообщение с ручной установкой возраста в формате "Установить возраст: xx" ------
            elif re.findall(r'Установить возраст:? ?\d+[- ]\d+', request, re.IGNORECASE):
                change_filter_age(id_user, request), send_message(vk, id_user, 'Возраст установлен')
                save_search_people(id_user, check=True)

            # ------ Нажатие на кнопку "Статус: нажать для получения информации" ------
            elif pay_load_type == 'info_status':                                            # Инфо про установку статуса
                send_message(vk, id_user, message_status()[1])

            # ------ Нажатие на кнопку "Город: нажать для получения информации" ------
            elif pay_load_type == 'info_city':                                              # Инфо про установку города
                send_message(vk, id_user, message_city()[1])

            # ------ Обработка сообщения в формате "статус <номер статуса>" ------
            elif re.findall(r'статус ?[: -]? ?\d', request, re.IGNORECASE):          # Установка статуса
                send_message(vk, id_user, change_filter_status(id_user, request))
                save_search_people(id_user, check=True)

            # ------ Обработка сообщения в формате "город <номер города>" ------
            elif re.findall(r'город ?[: -]? ?\d{1,3}', request, re.IGNORECASE):      # Установка города
                send_message(vk, id_user, change_filter_city(id_user, request))
                save_search_people(id_user, check=True)

            # ------ Вызов главное меню, если пользователь напишет "меню" ------
            elif request == "меню":                                                         # Сообщение "Меню"
                send_message(vk, id_user, 'Главное меню', main_menu(id_user))

            # ------ Все остальные сообщения ------
            else:                                                                           # Остальные сообщения
                send_message(vk, id_user, 'Я не понял текст. Используйте кнопки или введите слово "меню".')

    # Событие на нажатия callback кнопок
    if event.type == VkBotEventType.MESSAGE_EVENT:
        callback = event.object.payload.get('type')     # действие callback
        id_user = event.object.user_id                  # id пользователя

        # ------ События на переход по ссылке ------
        if callback == 'open_link':
            snow_snackbar(vk, event.object.event_id, id_user, event.object.peer_id, json.dumps(event.object.payload))

        # ------ События на всплывающее сообщение ------
        if callback == 'show_snackbar':
            mess_payload = event.object['payload']['text']
            snow_snackbar(vk, event.object.event_id, id_user, event.object.peer_id, json.dumps(event.object.payload))

            # ------ Если текст всплывающего сообщения содержит слово "очищен" ------
            if 'очищен' in mess_payload:
                if 'список избранного очищен' in mess_payload:
                    LikedListBD().delete_like_all_user(id_user=id_user)
                else:
                    BlackListBD().delete_black_all_user(id_user=id_user)
                vk_.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Список очищен',
                    conversation_message_id=event.obj.conversation_message_id,
                )

            # ------ Если текст всплывающего сообщения содержит слово "удален" или "добавлен" ------
            if 'удален' in mess_payload or 'добавлен' in mess_payload:
                info_user = get_message_search(id_user)
                name_user = info_user['message'][info_user['message'].find(':') + 2:info_user['message'].find('\n')]
                if mess_payload.find('черный список') > 0:                                  # Добавление в BlackList
                    BlackListBD().add_user_black_list(id_user,
                                                      info_user['id_user'],
                                                      name_user)
                if mess_payload.find('список избранного') > 0:                              # Добавление в LikedList
                    LikedListBD().add_like_user(id_user,
                                                info_user['id_user'],
                                                name_user)
                if mess_payload.find('из черного списка') > 0:                              # Удаление из BlackList
                    BlackListBD().delete_user_black_list(id_user,
                                                         info_user['id_user'])
                if mess_payload.find('из списка избранного') > 0:                           # Удаление из BlackList
                    LikedListBD().delete_like_user(id_user,
                                                   info_user['id_user'])

                # После добавления/удаления в список сообщение редактируется
                vk_.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=info_user['message'],
                    conversation_message_id=event.obj.conversation_message_id,
                    attachment=info_user['attachment'],
                    keyboard=search_inline(info_user['url_profile'], id_user, info_user['id_user']).get_keyboard()
                )

        # ------ Нажатие на кнопку "следующий человек" ------
        if callback == 'next_people':

            # --- Если следующей анкеты нет в кеше Redis, то достать данные из PostgresSQL ---
            if redis_person_is_current(id_user):
                save_search_people(id_user)  # Сохранение людей, если их нет
                info_user = get_message_search(id_user)                      # Информацию о первой найденной анкете
                redis_save_history(id_user, info_user, size=HISTORY_SIZE)    # Сохранение в историю анкет Redis
                SearchPeopleBd().delete_user(id_user, info_user['id_user'])  # Удаление прошлой записи
                redis_set_person(id_user, info_user)                         # Сохранить анкету в кэш
                redis_set_current_person(id_user, info_user['id_user'])      # Установить текущую просматриваемую анкету

            # --- Если в Redis есть информация о следующей анкете, то информация о человеке берётся из Redis ---
            else:
                info_user = redis_get_next_person(id_user)               # Информация об анкете
                redis_set_current_person(id_user, info_user['id_user'])  # Установить текущую просматриваемую анкету

            # Предыдущая анкета изменяется на новую анкету с текущими данными
            vk_.messages.edit(
                peer_id=event.obj.peer_id,
                message=info_user['message'],
                conversation_message_id=event.obj.conversation_message_id,
                attachment=info_user['attachment'],
                keyboard=search_inline(info_user['url_profile'], id_user, info_user['id_user']).get_keyboard()
            )

        # ------ Нажатие на кнопку "предыдущий человек" ------
        if callback == 'prev_people':
            info_user = redis_get_prev_person(id_user)

            # Если информация в кеше закончится, то кнопка "предыдущий человек" станет недоступной
            if info_user == 'end list':
                info_user = redis_get_person_info(id_user)
                prev_person = True
            # Если информация в кеше не закончилась, то можно вернуться к предыдущей анкете
            else:
                redis_set_current_person(id_user, info_user['id_user'])     # Установить текущую просматриваемую анкету
                prev_person = False

            # Предыдущая анкета изменяется на новую анкету с текущими данными
            vk_.messages.edit(
                peer_id=event.obj.peer_id,
                message=info_user['message'],
                conversation_message_id=event.obj.conversation_message_id,
                attachment=info_user['attachment'],
                keyboard=search_inline(info_user['url_profile'],
                                       id_user,
                                       info_user['id_user'],
                                       prev_person).get_keyboard()
            )
