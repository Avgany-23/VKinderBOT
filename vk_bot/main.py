from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dotenv import load_dotenv
import os


load_dotenv()


vk = vk_api.VkApi(token=os.getenv('main_token'))
longpoll = VkLongPoll(vk)


# def sender()


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            print(event.from_user)
            id_user = event.user_id
            request = event.text

            if request == "привет":
                write_msg(id_user, f"Хай, {id_user}")
            elif request == "пока":
                write_msg(id_user, "Пока((")
            else:
                write_msg(id_user, "Не поняла вашего ответа...")



# import requests
#
# access_token="...."
# token = access_token
# city_id = '1'
# age_from = '10'
# age_to = '20'
#
# url = f'https://api.vk.com/method/users.search?city={city_id}&age_from={age_from}&age_to={age_to}&count=400&access_token={token}&v=5.131'
# print(url)
# response = requests.get(url)
# data = response.json()
# count = 0
# if 'response' in data:
#     users = data['response']['items']
#     for user in users:
#         # print(user)
#         count += 1
# else:
#     print(data)
# print(count)