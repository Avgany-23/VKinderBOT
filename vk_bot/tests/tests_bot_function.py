from database.create_bd import delete_object_db
from test_settings import (TOKEN_BOT_TEST,
                           GROUP_ID_VK_TEST,
                           VK_ID_TEST,
                           PATH_TEST_POSTGRESQL,
                           test_BlackListBD,
                           test_LikedListBD,
                           test_UsersBd)
from function_for_test import list_users_test, test_connect_vk_bot, test_create_bd
from vk_api.bot_longpoll import VkBotLongPoll
from vk_bot.bot_function import send_message
from vk_bot import bot_function
from random import randrange
from unittest import skipIf
from vk_api import VkApi
from time import sleep
import unittest
import inspect
import vk_api


"""
Перед началом теста с функциями Бота, ему необходимо отправить сообщение в вк от id, которое указано
в test_settings.py для того, чтобы разрешить боту взаимодействовать с пользователем.
"""

test_go = test_connect_vk_bot(TOKEN_BOT_TEST, GROUP_ID_VK_TEST, VK_ID_TEST)
message_reason_bd = ('Неправильно указаны данные для тестового бота\n'
                     'Проверьте правильность token_bot_test, group_id_test и id_vk_for_test')
create_bd_status = test_create_bd(PATH_TEST_POSTGRESQL)


def tearDownModule():
    if create_bd_status:
        result = delete_object_db(PATH_TEST_POSTGRESQL)
        if result[0] == - 1:
            print(f'БД не удалена\n{result[1]}')


class TestMainFunction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        user = test_UsersBd
        another_user = [test_LikedListBD, test_BlackListBD]
        for id_ in range(1, 4):
            user.create_user(id_)

            for another_id, another_name in [
                (1, 'Валера'),
                (10, 'Игорь'),
                (100, 'Света')
            ]:
                another_user[0].add_like_user(id_, another_id, another_name)
                another_user[1].add_user_black_list(id_, another_id, another_name)

    @classmethod
    def tearDownClass(cls):
        user = test_UsersBd
        another_user = [test_LikedListBD, test_BlackListBD]
        for id_ in range(1, 4):
            user.delete_user(id_)
            another_user[0].delete_like_all_user(id_)
            another_user[1].delete_black_all_user(id_)

    @skipIf(not create_bd_status, 'База Данных не создана')
    def test_lists_user(self):
        print(create_bd_status)
        info = {'name': ['Имя: Валера', 'Имя: Игорь', 'Имя: Света'],
                'url': ['https://vk.com/id1', 'https://vk.com/id10', 'https://vk.com/id100']}
        for id_ in range(1, 4):
            with self.subTest(id_):
                result_like_list = list_users_test(id_)
                result_black_list = list_users_test(id_, list_user='Block list')
                for name in info['name']:
                    self.assertIn(name, result_like_list, f"--->'{name}' должно быть в {result_like_list}")
                    self.assertIn(name, result_black_list, f"--->'{name}' должно быть в {result_black_list}")


class TestCheckFunction(unittest.TestCase):
    def test_check_function_in_module(self):
        module_function = [func[0] for func in inspect.getmembers(bot_function, inspect.isfunction)]
        for i, func in enumerate([
            'send_message',
            'snow_snackbar',
            'list_users',
            'user_filters',
            'change_filter_age',
            'change_filter_sex',
            'change_filter_status',
            'change_filter_city',
            'marks_person',
            'get_message_search',
            'save_search_people',
            'get_id_vk_users_photo',
        ], 1):
            with self.subTest(i):
                self.assertIn(func, module_function,
                              f'Функция {func} должна быть в vk_bot.bot_function')


class TestBotToken(unittest.TestCase):
    def test_correct_test_token_and_id_group(self):
        """Проверка тестовых данных для работы тестов"""
        try:
            vk = VkApi(token=TOKEN_BOT_TEST)
            vk.get_api()
            VkBotLongPoll(vk, GROUP_ID_VK_TEST)
        except vk_api.exceptions.ApiError:
            raise AssertionError('Неверно указаны тестовый токен или group id для тестового бота')

    def test_correct_main_token_and_id_group(self):
        """Проверка основных данных для работы программы"""
        try:
            vk = VkApi(token=TOKEN_BOT_TEST)
            vk.get_api()
            VkBotLongPoll(vk, GROUP_ID_VK_TEST)
        except vk_api.exceptions.ApiError:
            raise AssertionError('Неверно указаны тестовый токен или group id для тестового бота')


class TestSendMessages(unittest.TestCase):
    vk = VkApi(token=TOKEN_BOT_TEST)
    vk.get_api()
    VkBotLongPoll(vk, GROUP_ID_VK_TEST)

    def setUp(self):
        sleep(0.5)

    @skipIf(not test_go, 'test_send_message\n' + message_reason_bd)
    def test_send_message_text(self):
        self.assertIsNone(send_message(vk=self.vk, user_id=VK_ID_TEST, message='test_send_message'),
                          'Функция send_message не должна ничего возвращать')

    @skipIf(not test_go, 'test_send_message\n' + message_reason_bd)
    def test_send_message_photo(self):
        try:
            send_message(vk=self.vk, user_id=VK_ID_TEST, message='test_send_message_photo',
                         attachment=['photo352099844_457239265'])
        except BaseException:
            raise AssertionError('Функция send_message_photo не смогла отправить сообщение с фотографией')

    @skipIf(not test_go, 'test_send_message\n' + message_reason_bd)
    def test_send_message_wrong_id_user(self):
        vk_id = int(VK_ID_TEST) + randrange(100, 100000)
        self.assertRaises(
            vk_api.exceptions.ApiError, send_message, self.vk,
            vk_id,
            'test_send_message_photo',
            attachment=['photo352099844_457239265']
        )
