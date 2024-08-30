# import requests
#
#
# api_token = 'vk1.a.J4b_aMrXQw9iv7Vv1qM67yyM3STTs2vCEEeei-oiEqWv-DfH8wkCxpLYWCRCtp4zn2B_oIQr-E9kN77yGxBjRkkOldMZNlRmF5DSRDJwC7KWC0lMoKhHnJMfhTdH6qysbgvcpzpwdtIVAGhhiDMvaAx6B2or_o11fLsCSF9bQEydjkM2miXld63ZrxfaNDd5'
# user_id = '119922158'  # открытый профиль но без даты рождения
# user_id_2 = '49293108'  # закрытый профиль но без даты рождения
#
# class SearchVK:
#     def __init__(self, token_api_vk, version='5.199'):
#         self.basic_url = 'https://api.vk.com/method/'
#         self.params = {'access_token': token_api_vk, 'v': version}
#
#     def get_user_vk(self, user_id):
#         params = {'user_ids': user_id,
#                   'fields': 'screen_name, sex, city, relation, activities, about, bdate, interests, music, activities'}
#         response = requests.get(self.basic_url + 'users.get', params={**params, **self.params})
#         return response.json()
#
#     def get_users_vk(self, count: int = 1000, **kwargs):
#         """
#         :param count: количество людей, которых нужно найти
#         :type kwargs:   sex: int (1 or 2)
#                         city: int,
#                         online: int (1 or 2),
#                         age_from: int,
#                         age_to: int,
#                         has_photo: int (0 or 1),
#                         is_closed: bool,
#                         fields: str.
#         """
#         params = {'count': count,
#                   **kwargs}
#         response = requests.get(self.basic_url + 'users.search', params={**params, **self.params})
#         if response.json().get('error'):
#             return response.json().get('error').get('error_msg')
#         return response.json()['response']['items']
#
#
#     def get_photo_user(self, user_id, place='profile', max_count=5):
#         params = {'owner_id': user_id,
#                   'album_id': place,
#                   'extended': 1,
#                   'count': max_count}
#         response = requests.get(self.basic_url + 'photos.get', params={**params, **self.params}).json()
#         try:
#             list_photos = {}
#             for photo in response['response']['items']:
#                 list_photos[photo['id']] = {
#                     'photo_url': photo['sizes'][-1]['url'],
#                     'likes': photo['likes']['count'],
#                 }
#         except KeyError as e:
#             return f'Произошла ошибка\n{e}'
#         return list_photos
#
#
# vk_get = SearchVK(api_token)
# user = vk_get.get_user_vk(user_id_2)  # Получение информации о пользователе по его user_id
# users = vk_get.get_users_vk(1000, sex=1, age_from=20, is_closed = False)    # Получение пользователей
# photo_user = vk_get.get_photo_user(user_id_2, place='wall', max_count=3)  # 3 фотки пользователя СО стены
# print(photo_user)