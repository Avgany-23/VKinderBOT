"""
####Документация по api_vk проекта VKinder

#создание файла конфигурации
config = configparser.ConfigParser()

#добавление секций, ключей и значений
config.add_section('VK')

#читаем файл с токенами, паролями и т.д.
config.read('config.ini')
access_token = config.get('VK', 'key')
token_2 = config.get('VK', 'user_access_key')
#не забываем положить config.ini в gitignore


##class VK
храним в нем часто используемые переменные
access_token #сервисный ключ доступа в приложении разработчика
user_id #идентификатор юзера, который должен иметь открытый профиль (доступ к фото) и полную дату рождения
token_2 #ключ доступа пользователя
version #версия
id_app #идентификатор приложения

##ФУНКЦИИ

def users_info(self)
запрос через requests, метод ВК users.get
получаем:screen_name, sex, city, relation, activities, about, bdate, interests, music, activities
возвращается json()

def get_photos_from_profile(self)
запрос через requests, метод ВК photos.get
ставим ограничения в запросе: фото из профиля, кол-во 3 шт, extended вернет дополнительные поля - likes
возвращается json()

def get_photos_from_wall(self)
идентично функции def get_photos_from_profile(self)
отличие: ставим ограничения в запросе - фото со стены
возвращается json()

def calculate_age(self, date_)
поскольку метод users.get не возвращает возраст, а только дату рождения, эта функция поможет вычислить возраст по дате рождения
возвращает возраст int

def formatting_sex(self, int_sex)
методы вк возвращают пол в булевом представлении:
sex 1: female, sex 2: male
функция форматирует пол в str
возвращает пол женский/мужской

def formatting_marital_status(self, int_relation)
методы вк возвращают семейное положение в булевом выражении:
0 не выбрано
1 не замужем/не женат
2 встречаюсь
3 помолвлен(а)
4 женат/замужем,
5 все сложно
6 в активном поиске
7 влюблен(а)
8 в гражданском браке
функция поможет переформатировать int в str
возвращает str

def formatting_users_info_and_photos_with_likes(self)
соберем массив, полученный о пользователе в словарь
создадим словарь-обертку, где ключом будет id юзера
создадим еще один словарь, который будет хранить ключи-значения
переберем массив, полученный о пользователе путем users_info() в цикле
назначим id основным ключом
добавляем в словарь со значениями данные из массива по очереди
не забываем про булевы значения, форматируем пол
обходим ошибку, если у пользователя не указана полная дата рождения
не забываем про булевы значения, форматируем семейное положение
обходим ошибку, если у пользователя приватный профиль
теперь переберем массив, полученный о пользователе путем get_photos_from_profile() в цикле
соберем в списки лайки, фото(ссылки), id фото
возвращает словарь

def generate_auth_url(self, id_app)
генератор ссылки,
Этот URL будет содержать информацию о приложении и необходимых разрешениях.
вернет ссылку, переходя по которой пользователь переходит на страницу с https://oauth.vk.com/blank.html#code-----
если у нас есть этот #code----- мы можем получить Ключ доступа пользователя
# app_id = ''  # ID твоего приложения
# client_secret = ''  # Защищенный ключ приложения
# redirect_uri = 'https://oauth.vk.com/blank.html'
# code = ''  # Код, полученный на предыдущем шаге
# url = 'https://oauth.vk.com/access_token'
# params = {
#     'client_id': app_id,
#     'client_secret': client_secret,
#     'redirect_uri': redirect_uri,
#     'code': code,
#     'scope': "photos"
# }
# response = requests.get(url, params=params)
# try:
#     data = response.json()  # Попытка получить JSON из ответа
#     if 'access_token' in data:
#         access_token = data['access_token']
#         expires_in = data['expires_in']  # Время жизни токена
#         user_id = data['user_id']  # ID пользователя
#         print("Access Token:", access_token)
#     else:
#         print("Ошибка получения токена:", data.get('error_description', 'Неизвестная ошибка'))
# except ValueError:
#     print("Ответ не является JSON:", response.text)  # Если не удалось декодировать как JSON

###ОБХОД ВКонтакте максимальная выдача при поиске — 1 000 человек, мы разделили поиск по гендерам
def find_users_woman(self)
функция, которая ищет женщин
запрос через requests, метод ВК users.search
переберем циклом те поля в users_info(), которые могут послужить совпадениями, получим переменные для params
обойдем ошибку при отсутсвии даты рождения в профиле

ставим ограничения в запросе: выдача - 1000, пол - женский, город- совпадение, онлайн - человек ответит скорее оперативнее + избегаем удаленные аккаунты
возраст от: возраст мужчины -10 лет, возраст до: возраст мужчины, только с фото, не замужем, все сложно, в активном поиске, открытый профиль
возвращается json()

def find_users_men(self)
функция, которая ищет мужчин
запрос через requests, метод ВК users.search
переберем циклом те поля в users_info(), которые могут послужить совпадениями, получим переменные для params
обойдем ошибку при отсутсвии даты рождения в профиле

ставим ограничения в запросе: выдача - 1000, пол - мужской, город- совпадение, онлайн - человек ответит скорее оперативнее + избегаем удаленные аккаунты
возраст от: возраст женщины, возраст до: возраст женщины + 10 лет, только с фото, не женат, все сложно, в активном поиске, открытый профиль
возвращается json()


def formatting_find_users_woman(self)
создать словарь
создать переменную, равную результатам поиска с помощью функции find_users_woman()
пройдемся циклом по переменной
назначим id пользователя первым ключом
в созданный словарь запишем данные о девушках
пройдемся циклом по id в созданном словаре
запрос через requests, метод ВК photos.get
обязательно включаем time.sleep(0.5), иначе упадет
создаем перменную woman_photo как ответ запроса
идем циклом по фото респонса(woman_photo)
в список добавляем ссылку на фото, кол-во лайков и айдишник фотографии
в созданный словарь вносим по ключу photo наш созданный список
возвращает словарь
ПРОБЛЕМА записывается только по одной фотке


def formatting_find_users_men(self)
соберем массив, полученный о пользователях-мужчинах в словарь
создадим словарь-обертку, где ключом будет id юзера
создадим еще один словарь, который будет хранить ключи-значения
переберем массив, полученный о пользователе путем find_users_men в цикле
назначим id основным ключом
добавляем в словарь со значениями данные из массива по очереди
не забываем про булевы значения, форматируем пол
обходим ошибку, если у пользователя не указана полная дата рождения
не забываем про булевы значения, форматируем семейное положение
обращаемся к методу photos.get запросом в функции, чтобы поменять owner_id на id_integer
(а не self.id, это важно. Нам нужны фото найденных мужчин, а не наши)
теперь переберем массив, полученный о пользователе путем men_photo = response.json() в цикле
соберем в списки лайки, фото(ссылки), id фото
обходим ошибку, если у пользователя приватный профиль
возвращает словарь
ПРОБЛЕМА - словарь с одним мужчиной в описании и разными фотографиями других мужчин


user_id = ''
vk = VK(access_token, user_id, token_2)
Пожалуйста, не забудьте, что у пользователя user_id должен быть открытый профиль с доступом к фото, указана полная дата рождения (день, месяц, год)
иначе код работать не будет, и никто не познакомится, все логично

"""