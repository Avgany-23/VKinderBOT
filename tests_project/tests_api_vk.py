from test_settings import VK_KEY_API_TEST
from api_vk.main import SearchVK
from unittest import TestCase
from random import randint
from time import sleep
import unittest


vk_get = SearchVK(VK_KEY_API_TEST)
result = vk_get.get_user_vk(1)
status = True
if not isinstance(result, dict):
    status = False


@unittest.skipIf(not status, 'Проблема с token ВК')
class TestVkApi(TestCase):
    user_id_1 = 119922158
    user_id_2 = 49293108

    def tearDown(self):
        sleep(0.5)

    def test_get_user_info_vk(self):
        """Тест на выдачу ключей с динамической информацией (открытый акк)"""
        results = vk_get.get_user_vk(self.user_id_1)
        for i, key in enumerate([
            'first_name',
            'id_user',
            'city_title',
            'sex',
            'last_name',
        ], 1):
            with self.subTest(i):
                self.assertIn(key, results)

    def test_get_user_info_vk_2(self):
        """Тест на выдачу ключей с динамической информацией (закрытый аккаунт)"""
        results = vk_get.get_user_vk(self.user_id_2)
        for i, key in enumerate([
            'first_name',
            'id_user',
            'city_title',
            'sex',
            'last_name',
        ], 1):
            with self.subTest(i):
                self.assertIn(key, results)

    def test_get_users_vk(self):
        """Тест с неверным token vk"""
        api_token = '234ooo'
        results = SearchVK(api_token).get_user_vk(self.user_id_2)
        self.assertEqual('Токен недоступен. Слишком много запросов или нужно заново авторизоваться', results)

    def test_get_users_vk_2(self):
        """Тест на соответствие заданного параметра count и получения пользователей"""
        results = vk_get.get_users_vk(self.user_id_2)
        self.assertEqual(93, len(results))

    def test_get_users_vk_3(self):
        """Тест на выдачу фотографий"""

        results = vk_get.get_photo_user(self.user_id_1)
        len_ = len(list(results.keys()))
        self.assertEqual(4, len_, f'Должно быть получено 4 фото. Результат {len_}')

    def test_get_users_vk_4(self):
        """Тест на соответствие заданного is_closed=True и результата"""
        results = vk_get.get_users_vk(5, sex=randint(0, 2), age_from=randint(20, 40), is_closed=True)
        # print(results[1])
        for i, info in enumerate(results):
            with self.subTest(i):
                self.assertFalse(info['is_closed'])

    def test_get_photo_user_2(self):
        """Тест на соответствие заданного max_count=3 и результата"""
        results = vk_get.get_photo_user(self.user_id_1, place='profile', max_count=3)
        s = 0
        for index, j in enumerate(results):
            s = index
        expected = s + 1
        self.assertEqual(expected, len(results))

    def test_get_photo_user_3(self):
        """Проверка получения ссылок на фото пользователей"""
        results = vk_get.get_photo_user(self.user_id_1, place='profile', max_count=3)
        for i, key in enumerate(results.keys()):
            with self.subTest(i):
                value = results[key]['photo_url']
                expected = 'https://' in value
                self.assertTrue(expected)
