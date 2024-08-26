"""
####Документация по api_vk проекта VKinder

###main.py

api_token = токен (сервисный ключ доступа), для get_users_vk обязательно ключ доступа пользователя

id для тестов
user_id_1 = '119922158'  # открытый профиль но без даты рождения
user_id_2 = '49293108'  # закрытый профиль, но с датой рождения

##class VK
Хранение базового URL, который используется в функциях-запросах с разными методами ВКонтакте

##Функции

def get_user_info_vk
получение информации о пользователе по его user_id
возвращает словарь с полями:
'screen_name, sex, city, relation, activities, about, bdate, interests, music, activities'

def get_users_vk
получение пользователей и информации о них, можно настраивать определенные фильтры
пол, город, статус "в сети", возраст от и до, профиль С фото или БЕЗ, открытый/закрытый профиль, поля:
'screen_name, sex, city, relation, activities, about, bdate, interests, music, activities'
обработка возможной ошибки - отображение текста ошибки

def get_photo_user
получение фото пользователя по его user_id
place на выбор:
wall — фотографии со стены,
profile — фотографии профиля,
saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя.
extended 1 — будут возвращены дополнительные поля likes, comments, tags, can_comment, reposts
Проходим циклом по ответу реквеста, помещаем ссылку на фото + кличество лайков в список
возвращаем список
возможная ошибка - возникновение в случае приватного профиля пользователя


####Redis_cash.py

1. Установка
a) macOS
brew install redis --установка
brew services list --проверка
brew services start redis --запуск
redis-cli --локальное подключение
ввод в консоли PING
ответ PONG --все работает
brew services stop redis --остановка redis

б) WIN
doker run -d -p 6379:6379 redis --запуск контейнера с redis
doker container ps
docker exec -it <вставить сюда без скобок статус слева от редиса> redis-cli
ввод в консоли PING
ответ PONG --все работает
doker container stop <аналогичный номер тремя строками выше>

"""