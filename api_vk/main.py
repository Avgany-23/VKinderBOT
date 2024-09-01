from settings import VK_VERSION
import requests


class SearchVK:
    def __init__(self, token_api_vk: str) -> None:
        self.basic_url = 'https://api.vk.com/method/'
        self.params = {'access_token': token_api_vk, 'v': VK_VERSION}

    def get_user_vk(self, user_id: int) -> str | dict:
        """Функция возвращает информацию о пользователе в ВК по его user_id"""
        params = {'user_ids': user_id,
                  'fields': 'screen_name, sex, city, relation, activities, about, bdate, interests, music, activities'}

        try:
            response = requests.get(self.basic_url + 'users.get',
                                    params={**params, **self.params}).json()['response'][0]
        except KeyError:
            return 'Токен недоступен. Слишком много запросов или нужно заново авторизоваться'
        city = response.pop('city', {'title': 'не установлен', 'id': 0})
        id_user = response.pop('id')
        return {'city_title': city['title'], 'id_user': id_user, **response, 'city_id': city['id']}

    def get_users_vk(self, count: int = 1000, **kwargs) -> dict:
        """
        :param count: количество людей, которых нужно найти
        :type kwargs:   sex: int (1 or 2)
                        city: int,
                        online: int (1 or 2),
                        age_from: int,
                        age_to: int,
                        has_photo: int (0 or 1),
                        is_closed: bool,
                        fields: str,
                        is_closed: boole.
        """
        params = {'count': count,
                  **kwargs}
        response = requests.get(self.basic_url + 'users.search', params={**params, **self.params})
        if response.json().get('error'):
            return response.json().get('error').get('error_msg')
        return response.json()['response']['items']

    def get_photo_user(self, user_id: int, place='profile', max_count: int = 5) -> dict | int:
        """place in ('profile', 'wall')"""
        params = {'owner_id': user_id,
                  'album_id': place,
                  'extended': 1,
                  'count': max_count,
                  'rev': 1}
        response = requests.get(self.basic_url + 'photos.get', params={**params, **self.params}).json()
        try:
            list_photos = {}
            for photo in response['response']['items']:
                list_photos[photo['id']] = {
                    'photo_url': photo['sizes'][-1]['url'],
                    'likes': photo['likes']['count'],
                }
            return list_photos
        except KeyError:
            return -1
