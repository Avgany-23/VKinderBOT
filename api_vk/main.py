import requests
import configparser
from pprint import pprint
from datetime import datetime, date
import datetime
import time


config = configparser.ConfigParser()
config.add_section('VK')
config.read('config.ini')
access_token = config.get('VK', 'key')
token_2 = config.get('VK', 'user_access_key')





class VK:
  def __init__(self, access_token, user_id, token_2, version='5.199', id_app='51927413'):
      self.token = access_token
      self.id = user_id
      self.version = version
      self.params = {'access_token': self.token, 'v': self.version}
      self.id_app = id_app
      self.token_2 = token_2

  def users_info(self):
      url = 'https://api.vk.com/method/users.get'
      params = {'user_ids': self.id,
                'fields': 'screen_name, sex, city, relation, activities, about, bdate, interests, music, activities'}
      response = requests.get(url, params={**self.params, **params})
      return response.json()


  def get_photos_from_profile(self):
      url = 'https://api.vk.com/method/photos.get'
      params = {'owner_id': self.id,
                'access_token': self.token,
                'album_id': 'profile',
                'extended': 1,
                'count': 3}
      response = requests.get(url, params={**self.params, **params})
      if 'error' in str(response.json().items()):
          return response.json()['error']['error_msg']
      return response.json()

  def get_photos_from_wall(self):
      url = 'https://api.vk.com/method/photos.get'
      params = {'owner_id': self.id,
                'access_token': self.token,
                'album_id': 'wall',
                'extended': 1,
                'count': 2}
      response = requests.get(url, params={**self.params, **params})
      if 'error' in str(response.json().items()):
          return response.json()['error']['error_msg']
      return response.json()

  def calculate_age(self, date_):
      self.date_ = date_
      today_date = date.today()
      date_str = date_
      date_time_obj = datetime.datetime.strptime(date_str, '%d.%m.%Y')
      normal_date = date_time_obj.date()
      age = int(((today_date - normal_date).days) / 365)
      return age


  def formatting_sex(self, int_sex):
      self.int_sex = int_sex
      sex = ''
      if int_sex == 1:
          sex = 'женский'
      elif int_sex == 2:
          sex = 'мужской'
      return sex

  def formatting_marital_status(self, int_relation):
      self.int_relation = int_relation
      relation = ''
      if int_relation == 0:
          relation = "Не выбрано"
      elif int_relation == 1:
          if self.int_sex == 1:
              relation = "не замужем"
          if self.int_sex == 2:
              relation = 'не женат'
      elif int_relation == 2:
          relation = "встречаюсь"
      elif int_relation == 3:
          if self.int_sex == 1:
              relation = "помолвлена"
          if self.int_sex == 2:
              relation = "помолвлен"
      elif int_relation == 4:
          if self.int_sex == 1:
              relation = "замужем"
          if self.int_sex == 2:
              relation = "женат"
      elif int_relation == 5:
          relation = "все сложно"
      elif int_relation == 6:
          relation = "в активном поиске"
      elif int_relation == 7:
          if self.int_sex == 1:
              relation = "влюблена"
          if self.int_sex == 2:
              relation = "влюблен"
      elif int_relation == 8:
          relation = "в гражданском браке"
      return relation

  def formatting_users_info_and_photos_with_likes(self):
      dict_with_users_info = {}
      dict_values = {}
      for info in vk.users_info()['response']:
          id_integer = info['id']
          dict_with_users_info[id_integer] = dict_values
          dict_values['first_name'] = info['first_name']
          dict_values['last_name'] = info['last_name']
          dict_values['sex'] = vk.formatting_sex(info['sex'])
          try:
              dict_values['age'] = vk.calculate_age(info['bdate']) #обход ошибки юзеров, кто не указывал дату рождения
          except KeyError:
              dict_values['age'] = "Возраст был скрыт пользователем"
          dict_values['city'] = info['city']['title']
          dict_values['relation'] = vk.formatting_marital_status(info['relation'])
          dict_values['about'] = info['about']
          dict_values['activities'] = info['activities']
          dict_values['interests'] = info['interests']
          dict_values['favorite_music'] = info['music']
          dict_values['id_screen_name'] = info['screen_name']
          try:
              for photo in vk.get_photos_from_profile()['response']['items']:
                  list_photo = []
                  list_likes = []
                  photo_url = photo['sizes'][-1]['url']
                  list_photo.append(photo_url)
                  likes = photo['likes']['count']
                  id_photo_p = photo['id']
                  list_likes.append(likes)
                  for p, l in zip(list_photo, list_likes):
                      dict_values[f'фото из профиля {p}'] = f'лайки {l}, id_photo {id_photo_p}'
              for wall_photo in vk.get_photos_from_wall()['response']['items']:
                  l_photo = []
                  l_likes = []
                  url = wall_photo['sizes'][-1]['url']
                  l_photo.append(url)
                  like = wall_photo['likes']['count']
                  l_likes.append(like)
                  id_photo_w = photo['id']
                  for ph, li in zip(l_photo, l_likes):
                      dict_values[f'фото со стены {ph}'] = f'лайки {li}, id_photo {id_photo_w}'
          except KeyError:
              dict_values["photo"] = "Фото профиля недоступны, профиль закрыт"
          except TypeError:
              dict_values["photo"] = "Фото профиля недоступны, профиль закрыт"
      return dict_with_users_info

  # это генератор ссылки, перейдя по которой встречаем окно "продолжить как..."
  def generate_auth_url(self, id_app):
      scope = "offline"  # Права доступа: 'offline' означает, что токен будет работать даже после завершения сессии
      redirect_uri = "https://oauth.vk.com/blank.html"  # URL на который будет перенаправлен пользователь после авторизации
      # Формируем URL
      auth_url = (
          f"https://oauth.vk.com/authorize?"
          f"client_id={id_app}&"
          f"display=page&"
          f"redirect_uri={redirect_uri}&"
          f"scope={scope}&"
          f"response_type=code&"
          f"v=5.199"  # Версия API
      )
      return auth_url

  def find_users_woman(self):
      url = 'https://api.vk.com/method/users.search'
      for info in vk.users_info()['response']:
          city = info['city']['id']
          try:
              age = vk.calculate_age(info['bdate']) #обход ошибки юзеров, кто не указывал дату рождения
          except KeyError:
              return "Мы не знаем Ваш возраст, чтобы осуществить поиск пары"
      params = {'access_token': token_2,
            'count': 10, #поменять на 1000
            'sex': 1, #ищем женщин
            'city': city,
            'online': 1,
            'age_from': age - 10, #искать младше мужчины на 10 лет
  """здесь надо настроить фильтр бота чтоб переменную (- 10) менять на предпочтения мужчин"""
            'age_to': age,  # искать до возраста мужчины, не старше
            'has_photo': 1, #искать только с фото
            'status': (1, 5, 6),  # не замужем, все сложно, в активном поиске
            'is_closed': False,
            'fields': 'screen_name, sex, city, relation, activities, about, bdate, interests, music, activities'}
      response = requests.get(url, params={**self.params, **params})
      return response.json()



  def find_users_men(self):
      url = 'https://api.vk.com/method/users.search'
      for info in vk.users_info()['response']:
          city = info['city']['id']
          try:
              age = vk.calculate_age(info['bdate']) #обход ошибки юзеров, кто не указывал дату рождения
          except KeyError:
              return "Мы не знаем Ваш возраст, чтобы осуществить поиск пары"
          params = {'access_token': token_2,
            'count': 10, #поменять на 1000
            'sex': 2, #ищем мужчин
            'city': city,
            'online': 1,
            'age_from': age, #искать от возраста женщины
  """здесь надо настроить фильтр бота чтоб переменную (+ 10) менять на предпочтения женщин"""
            'age_to': age + 10, #искать старше на 10 лет, не более
            'has_photo': 1, #искать только с фото
            'status': (1, 5, 6), #не женат, все сложно, в активном поиске
            'is_closed': False,
            'fields': 'screen_name, city, sex, relation, activities, about, bdate, interests, music, activities'}
      response = requests.get(url, params={**self.params, **params})
      return response.json()

  def formatting_find_users_woman(self):
      dict_with_woman = {}
      woman = vk.find_users_woman()['response']['items']
      for w in woman:
          id_integer = w['id']
          dict_with_woman[id_integer] = {
              'first_name': w.get('first_name', ''),
              'last_name': w.get('last_name', ''),
              'sex': w.get('sex', ''),
              'about': w.get('about', ''),
              'activities': w.get('activities', ''),
              'bdate': w.get('bdate', ''),
              'city': w.get('city', ''),
              'favorite_music': w.get('favorite_music', ''),
              'screen_name': w.get('screen_name', ''),
              'interests': w.get('interests', ''),
              'relation': w.get('relation', ''),
              'photo': []
          }
          for id in dict_with_woman:
              w_url = 'https://api.vk.com/method/photos.get'
              time.sleep(0.5)
              params = {'owner_id': id,
                        'access_token': self.token,
                        'album_id': 'profile',
                        'extended': 1,
                        'count': 5}
              response = requests.get(w_url, params={**self.params, **params})
              woman_photo = response.json()
              try:
                  for photo in woman_photo['response']['items']:
                      list_photo_likes_id = []
                      photo_url = photo['sizes'][-1]['url']
                      likes = photo['likes']['count']
                      id_photo_p = photo['id']
                      list_photo_likes_id.append(photo_url)
                      list_photo_likes_id.append(f'лайки {likes} ')
                      list_photo_likes_id.append(f'фото id {id_photo_p} ')
                  dict_with_woman[id]['photo'] = list_photo_likes_id
              except KeyError:
                  return 'error'

      return dict_with_woman



  def formatting_find_users_men(self):
      dict_with_men = {}
      dict_values = {}
      for info in vk.find_users_men()['response']['items']:
          id_integer = info['id']
          dict_with_men[id_integer] = dict_values
          dict_values['first_name'] = info['first_name']
          dict_values['last_name'] = info['last_name']
          dict_values['sex'] = vk.formatting_sex(info['sex'])
          try:
              dict_values['age'] = vk.calculate_age(info['bdate'])  # обход ошибки юзеров, кто не указывал дату рождения
          except KeyError:
              dict_values['age'] = "Возраст был скрыт пользователем"
          except ValueError:
              dict_values['age'] = "Возраст был скрыт пользователем"
          dict_values['city'] = info['city']['title']
          dict_values['relation'] = vk.formatting_marital_status(info['relation'])
          dict_values['about'] = info['about']
          dict_values['activities'] = info['activities']
          dict_values['interests'] = info['interests']
          dict_values['favorite_music'] = info['music']
          dict_values['id_screen_name'] = info['screen_name']

          m_url = 'https://api.vk.com/method/photos.get'
          params = {'owner_id': id_integer,
                    'access_token': self.token,
                    'album_id': 'profile',
                    'extended': 1,
                    'count': 3}
          response = requests.get(m_url, params={**self.params, **params})
          men_photo = response.json()
          try:
              for photo in men_photo['response']['items']:
                  list_photo = []
                  list_likes = []
                  photo_url = photo['sizes'][-1]['url']
                  list_photo.append(photo_url)
                  likes = photo['likes']['count']
                  list_likes.append(likes)
                  id_photo_p = photo['id']
                  for p, l in zip(list_photo, list_likes):
                      dict_values[f'фото из профиля {p}'] = f'лайки {l}, id_photo {id_photo_p}'
          except KeyError:
              dict_values["photo"] = "Фото профиля недоступны, профиль закрыт"
      return dict_with_men





user_id = '49293108' #закрытый профиль, но с датой рождения
user_id_2 = '119922158' #открытый профиль но без даты рождения

vk = VK(access_token, user_id, token_2)
# vk = VK(access_token, user_id_2, token_2)





# pprint(vk.users_info()) #оба
# pprint(vk.get_photos_from_profile()) #оба
# pprint(vk.get_photos_from_wall()) #оба
# pprint(vk.calculate_age('25.12.1990')) #оба
# pprint(vk.formatting_sex(2)) #оба
# pprint(vk.formatting_marital_status()) #в словари все правильно передает
# pprint(vk.formatting_users_info_and_photos_with_likes())
# pprint(vk.generate_auth_url('51927413')) #оба
# pprint(vk.find_users_woman()) #оба
# pprint(vk.find_users_men()) #оба
# pprint(vk.formatting_find_users_woman())
# pprint(vk.formatting_find_users_men())