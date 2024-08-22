from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dotenv import load_dotenv
import os


load_dotenv()


vk = vk_api.VkApi(token=os.getenv('main_token'))
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    print(user_id)
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
