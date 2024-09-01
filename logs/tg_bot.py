from database.requests_redis import redis_connect
from settings import tg_bot
import threading
import schedule
import telebot
import time
import os


def bot_notification_tg() -> None:
    login_developer = tg_bot['data']['login']
    password_developer = tg_bot['data']['password']
    token_bot = tg_bot['data']['token']
    send_times = tg_bot['send_times']

    # Инициализация бота
    bot = telebot.TeleBot(token_bot)
    print('TG bot is working...')

    @bot.message_handler(commands=['start'])
    def send_welcome(message) -> None:
        unique_id_user = message.chat.id
        bot.send_message(unique_id_user, f'Привет! Вот список доступных команд:\n'
                                         f'/authorization  - чтобы авторизоваться\n'
                                         f'/times {" "*15}- чтобы посмотреть время, когда отправляются логи')

    @bot.message_handler(commands=['authorization'])
    def request(message) -> None:
        user_id = message.chat.id
        authorization_status = str(user_id) in redis_connect().lrange('tg_bot_users_id', 0, -1)
        if authorization_status:
            bot.send_message(message.chat.id, 'Ты уже авторизован 🙃')
        else:
            bot.reply_to(message, 'Введи логин: ')
            bot.register_next_step_handler(message, login)

    @bot.message_handler(commands=['times'])
    def request(message) -> None:
        user_id = message.chat.id
        authorization_status = str(user_id) in redis_connect().lrange('tg_bot_users_id', 0, -1)

        if authorization_status:
            times_logs = "\n".join(f'---{times}---' for times in send_times)
            message_chat = (f'Логи о критических ошибка приходят моментально.\n\n'
                            f'Уведомления стандартных логов приходят ежедневно по МСК в '
                            f'следующее время 🕘:\n{times_logs}\n'
                            f'Чтобы изменить время приходя стандартных логов, необходимо изменить их параметры:\n'
                            f'{" "*5}➡️ модуль settings ➡️ словарь tg_bot ➡️ ключ send_times')
        else:
            message_chat = 'Для просмотра id сначала нужно авторизоваться'

        bot.send_message(user_id, message_chat)

    def login(message) -> None:
        """Функция срабатывает после отправки пользователем логина в чат к боту"""
        if login_developer == message.text:
            bot.reply_to(message, 'Введи пароль: ')
            bot.register_next_step_handler(message, password)
        else:
            bot.reply_to(message, 'Такого логина нет, '
                                  'для повторного входа введите команду /authorization')

    def password(message) -> None:
        """Функция срабатывает после отправка пароля пользователем в чат к боту"""
        if password_developer == message.text:
            if str(message.chat.id) in redis_connect().lrange('tg_bot_users_id', 0, -1):
                bot.reply_to(message, f'Вы уже авторизованы ✅. Уведомления приходят ежедневно'
                                      f'в {", ".join(send_times)} по МСК.')

            else:
                bot.reply_to(message, f'Доступ открыт. Я присылаю файл с логами ежедневно в '
                                      f'{", ".join(send_times)} по МСК. А логи о критических ошибках будут присланы'
                                      f'сразу же.'
                                      f'Ты получишь файл в этом чате.')
                redis_connect().lpush(f'tg_bot_users_id', message.chat.id)
        else:
            bot.reply_to(message, 'Неверный пароль, для повторной попытки, перейди на команду /continue')

    def send_file(path: str, message: str) -> None:
        """Функция для отправки файла в чат к пользователю"""
        res_to_logs = os.path.join('logs', path)
        res_path = os.path.abspath(res_to_logs)
        if os.path.exists(res_path):
            status_send = True
            users_tg_id = redis_connect().lrange('tg_bot_users_id', 0, -1)

            # --- Проверка того, что файл не пустой ---
            with open(res_path, encoding='utf-8') as f:
                if not f.read():
                    status_send = False

            # --- Если файл не пустой, то отправить файл с логами ---
            if status_send and users_tg_id:
                for user in users_tg_id:
                    user = int(user)
                    bot.send_message(chat_id=user, text=message)
                    with open(res_path, encoding='utf-8') as f:
                        bot.send_document(chat_id=user, document=f)

                # --- Очистка файла, чтобы предотвратить отправку пустого файла ---
                with open(res_path, 'w', encoding='utf-8') as f:
                    f.truncate()

    def schedule_job_basic_log() -> None:
        """Функция для отправки уведомлений"""

        test_critical_error = 'В программе обнаружены критические ошибки❗️❗️❗️❗️❗️\nФайл с ними отправлен ниже'
        test_base_message = 'Отправка логов программы'
        text_starts_program = 'Старт вк бота'
        [schedule.every().day.at(times).do(job_func=send_file,
                                           path='logs_base.log',
                                           message=test_base_message) for times in send_times]

        while True:
            schedule.run_pending()
            send_file(path='logs_error.log', message=test_critical_error)
            send_file(path='starts_program.log', message=text_starts_program)
            time.sleep(60)

    # Для параллельного запуска с ботом
    schedule_job_thread = threading.Thread(target=schedule_job_basic_log)
    schedule_job_thread.start()

    try:
        bot.infinity_polling(skip_pending=True)
    except telebot.apihelper.ApiTelegramException as e:
        print(e)
