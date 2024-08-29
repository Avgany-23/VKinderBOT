import schedule
import time
import threading
import telebot
from tests_ import logger2


TOKEN_bot = ''
link_bot = 't.me/LogByVKinderBot.'
chat_id = '478646759'
login_developer = ''
password_developer = ''


# Инициализация бота
bot = telebot.TeleBot(TOKEN_bot)
print('Bot is working...')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    unique_id_user = message.chat.id
    bot.send_message(unique_id_user, 'Привет! Тебе нужно зарегистрироваться, чтобы получать логи VKinder_bot. '
                                     'Если ты наш разработчик, выбери команду /continue')


@bot.message_handler(commands=['continue'])
def request(message):
    bot.reply_to(message, 'Введи логин: ')
    bot.register_next_step_handler(message, login)

def login(message):
    user_text = message.text
    if login_developer == user_text:
        bot.reply_to(message, 'Введи пароль: ')
        bot.register_next_step_handler(message, password)
    else:
        bot.reply_to(message, 'Такого логина нет, пока')
        bot.register_next_step_handler(message, send_welcome)

def password(message):
    user_text_2 = message.text
    if password_developer == user_text_2:
        bot.reply_to(message, f'Доступ открыт. Я присылаю файл с логами ежедневно, 2 раза в день, '
                              f'09:00 и 20:00 по МСК. Ты получишь файл в этом чате.')
        schedule_job_thread = threading.Thread(target=schedule_job)
        schedule_job_thread.start()
    else:
        bot.reply_to(message, 'Неверный пароль, для повторной попытки, перейди на команду /continue')


def send_file():
    try:
        with open('tests.log', 'rb') as file:
            bot.send_document(chat_id=chat_id, document=file)
            logger2.info("Файл успешно отправлен.")
    except Exception as e:
        logger2.error(f"Ошибка при отправке файла: {e}")

def schedule_job():
    schedule.every().day.at("09:00").do(send_file)  # Первая рассылка в 09:00
    schedule.every().day.at("20:00").do(send_file)  # Вторая рассылка в 20:00

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)

