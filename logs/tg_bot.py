import schedule
import time
import threading
import telebot
from settings import tg_bot


def bot_notification_tg() -> None:
    main_id = tg_bot['data']['main_user_tg_id']
    chat_id_all = tg_bot['data']['all_ids_user']
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
        bot.send_message(unique_id_user, 'Привет! Тебе нужно авторизоваться, чтобы получать логи VKinder_bot. '
                                         'Если ты наш разработчик, выбери команду /continue')

    @bot.message_handler(commands=['continue'])
    def request(message) -> None:
        bot.reply_to(message, 'Введи логин: ')
        bot.register_next_step_handler(message, login)

    def login(message) -> None:
        user_text = message.text
        if login_developer == user_text:
            bot.reply_to(message, 'Введи пароль: ')
            bot.register_next_step_handler(message, password)
        else:
            bot.reply_to(message, 'Такого логина нет, пока')
            bot.register_next_step_handler(message, send_welcome)

    def password(message) -> None:
        user_text_2 = message.text
        if password_developer == user_text_2:
            bot.reply_to(message, f'Доступ открыт. Я присылаю файл с логами ежедневно в '
                                  f'{", ".join(send_times)} по МСК. '
                                  f'Ты получишь файл в этом чате.')
            schedule_job_thread = threading.Thread(target=schedule_job)
            schedule_job_thread.start()
        else:
            bot.reply_to(message, 'Неверный пароль, для повторной попытки, перейди на команду /continue')

    def send_file() -> None:
        with open(r'logs\file.txt', 'rb') as file:
            for user in chat_id_all:
                try:
                    bot.send_document(chat_id=user, document=file)
                except telebot.apihelper.ApiTelegramException:
                    bot.send_message(main_id, f'Пользователь с tg_id = {user} не начал диалог с ботом. '
                                              f'Логи на данный id не отправлены')

    def schedule_job() -> None:
        [schedule.every().day.at(times).do(send_file) for times in send_times]

        while True:
            schedule.run_pending()
            time.sleep(1)

    try:
        bot.infinity_polling(skip_pending=True)
    except telebot.apihelper.ApiTelegramException as e:
        print(e)
