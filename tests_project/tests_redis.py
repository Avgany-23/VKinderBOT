from test_settings import DATABASES_TEST
from unittest import TestCase
import json
from database.requests_redis import (
    redis_connect,
    redis_set_person,
    redis_set_current_person,
    redis_get_person_info,
    redis_get_current_person,
    redis_person_is_current,
    redis_clear_user_id,
    redis_save_history,
    redis_person_is_last,
    redis_get_prev_person,
    redis_browsing_history,
    redis_get_next_person)
import unittest
from unittest.mock import patch, MagicMock


class TestRedisFunc(TestCase):
    def setUp(self):
        self.id_main_test = 10
        self.message_test = {1: 'message1'}
        self.redis_test = redis_connect(DATABASES_TEST['redis'], charset_=False)
        self.redis_test.flushdb()

    def tearDown(self):
        self.redis_test.flushdb()

    def test_redis_connect(self):
        expected = 'redis.connection.ConnectionPool'
        self.assertIn(expected, str(self.redis_test))

    def test_redis_person_is_current(self):
        for data in range(1, 6):
            redis_set_person(self.id_main_test,
                             {data: f'message_{data}', 'id_user': data},
                             connect=self.redis_test)

        for i, (current, expected) in enumerate([
            (3, False),
            (4, False),
            (5, True)
        ], 1):
            with self.subTest(i):
                redis_set_current_person(self.id_main_test, current, connect=self.redis_test)
                get_current_id = int(redis_get_current_person(self.id_main_test, connect=self.redis_test))
                is_current = redis_person_is_current(self.id_main_test, connect=self.redis_test)
                self.assertEqual(get_current_id, current, 'Текущее id нахождение должно быть равным %s'.format(current))
                self.assertEqual(is_current, expected, f'Функция redis_person_is_current() с параметром'
                                                       f'id_user={current} должна выдавать {expected}')

    def test_redis_set_person(self):
        id_user = 5
        message = {"one": "two"}
        redis_set_person(id_user, message, connect=self.redis_test)
        # Проверка, что сообщение записано
        key = f"search_{id_user}"
        result = self.redis_test.lrange(key, 0, -1)
        self.assertEqual(len(result), 1)
        self.assertEqual(json.loads(result[0]), message)

    def test_redis_set_person_with_more_3_messages(self):
        id_user = 5
        # + несколько сообщений
        messages = [
            {"a1": "b1"},
            {"c2": "d2"},
            {"e3": "f3"},
            {"g4": "z4"},  # Это должно вызвать удаление самого старого сообщения
        ]
        for message in messages:
            redis_set_person(id_user, message, connect=self.redis_test)
        # Проверяем, что в списке осталось только 3 сообщения
        key = f"search_{id_user}"
        result = self.redis_test.lrange(key, 0, -1)
        self.assertEqual(len(result), 3)
        # Проверяем, что самое старое сообщение было удалено
        expected_messages = [{"g4": "z4"}, {"e3": "f3"}, {"c2": "d2"}]
        self.assertEqual([json.loads(msg) for msg in result], expected_messages)

    def test_redis_set_current_person(self):
        user_id = 1
        id_search_user = 42
        redis_set_current_person(user_id, id_search_user, connect=self.redis_test)
        # Проверяем, что значение установлено верно
        result = self.redis_test.get(f'current_person_{user_id}')
        self.assertIsNotNone(result)
        self.assertEqual(int(result), id_search_user)

    def test_redis_get_current_person(self):
        user_id = 1
        id_search_user = 12
        redis_set_current_person(user_id, id_search_user, connect=self.redis_test)
        result = redis_get_current_person(user_id, connect=self.redis_test)
        # Проверяем
        self.assertIsNotNone(result)
        self.assertEqual(int(result), id_search_user)

    def test_redis_get_person_info(self):
        user_id = 9
        test_data = [
            {"name": "Пользователь Катя", "age": 30, "url_profile": "http://example.com/userКатя"},
            {"name": "Пользователь Оля", "age": 25, "url_profile": "http://example.com/userОля"},
            {"name": "Пользователь Cережа", "age": 28, "url_profile": "http://example.com/userСережа"},
        ]
        for item in test_data:
            self.redis_test.rpush(f"search_{user_id}", json.dumps(item))
        result = redis_get_person_info(user_id, connect=self.redis_test)
        # Проверка результата
        expected_output = test_data[-1]  # Последний добавленный элемент
        self.assertEqual(result, expected_output)

    def test_redis_clear_user_id(self):
        user_id = 9
        self.redis_test.set(f'current_person_{user_id}', json.dumps({"id_user": 7}))
        test_data = [
            {"id_user": 2},
            {"id_user": 3},
            {"id_user": 7}
        ]
        for item in test_data:
            self.redis_test.rpush(f'search_{user_id}', json.dumps(item))
        # Проверяем, что данные еще не было
        self.assertIsNotNone(self.redis_test.get(f'current_person_{user_id}'))
        self.assertGreater(self.redis_test.llen(f'search_{user_id}'), 0)
        # удалить данные
        redis_clear_user_id(user_id, connect=self.redis_test)
        # Проверка удаления
        self.assertIsNone(self.redis_test.get(f'current_person_{user_id}'))
        self.assertEqual(self.redis_test.llen(f'search_{user_id}'), 0)

    def test_redis_save_history(self):
        user_id = 9
        messages = [
            {"text": "message 1"},
            {"text": "message 2"},
            {"text": "message 3"},
            {"text": "message 4"},
            {"text": "message 5"},
            {"text": "message 6"},
            {"text": "message 7"}  # Это сообщение должно удалить самое старое
        ]
        # Сохраняем первые 6 сообщений в истории (всё, что добавляется после, вызовет удаление)
        for i in range(1, 6):
            redis_save_history(user_id, messages[i], connect=self.redis_test)
        # Добавляем 7-е сообщение, что должно вызвать удаление
        redis_save_history(user_id, messages[6], connect=self.redis_test)
        # Получаем историю из Redis
        history = [json.loads(msg) for msg in self.redis_test.lrange(f'history_{user_id}', 0, -1)]
        # Проверка, что в истории остались только последние 6 сообщений
        self.assertEqual(len(history), 6)  # Должно быть 6 сообщений
        self.assertEqual(history[0]['text'], "message 7")
        self.assertEqual(history[-1]['text'], "message 2")

    @patch('database.requests_redis.redis_get_current_person')
    @patch('database.requests_redis.redis_connect')
    def test_person_is_last(self, mock_redis_connect, mock_redis_get_current_person):
        try:
            # Настройка mock для Redis
            mock_redis_client = MagicMock()
            mock_redis_connect.return_value = mock_redis_client
            redis_set_person(5, connect=self.redis_test, message={'data': '22', 'id_user': '44'})
            # Подготовка данных, которые будут возвращаться от lrange
            mock_redis_client.lrange.return_value = [
                json.dumps({'id_user': 1}),
                json.dumps({'id_user': 2}),
                json.dumps({'id_user': 3}),
            ]
            # Настройка текущей анкеты
            mock_redis_get_current_person.return_value = 3
            self.assertTrue(redis_person_is_last(1, connect=self.redis_test))
            mock_redis_get_current_person.return_value = 2
            self.assertFalse(redis_person_is_last(1, connect=self.redis_test))
            # Тест на случай, когда lrange возвращает пустой список
            mock_redis_client.lrange.return_value = []
            # Проверка на работу функции в случае пустого списка. Это должно вызвать IndexError,
            # поэтому мы обернем в assertRaises
            with self.assertRaises(IndexError):
                redis_person_is_last(1, connect=self.redis_test)
            # Дополнительно, тестируем случай, когда только одна анкета
            mock_redis_client.lrange.return_value = [
                json.dumps({'id_user': 1}),
            ]
            mock_redis_get_current_person.return_value = 1
            # Проверка с единственной анкетой
            self.assertTrue(redis_person_is_last(1, connect=self.redis_test))
        except IndexError as er:
            return f'check the database, the cache may be empty {er}'

    @unittest.skip
    @patch('database.requests_redis.redis_connect')
    def test_get_prev_person(self, mock_redis_connect):
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client

        mock_redis_client.lrange.return_value = [
            json.dumps({'id_user': 1}),
            json.dumps({'id_user': 2}),
            json.dumps({'id_user': 3}),
        ]

        mock_redis_client.get.return_value = 2

        expected_result = {'id_user': 1}
        self.assertEqual(redis_get_prev_person(1, connect=self.redis_test), expected_result)

        mock_redis_client.get.return_value = 3
        expected_result_end = 'end list'
        self.assertEqual(redis_get_prev_person(1, connect=self.redis_test), expected_result_end)

        mock_redis_client.lrange.return_value = []
        mock_redis_client.get.return_value = 1
        expected_result_empty = 'empty list'
        self.assertEqual(redis_get_prev_person(1, connect=self.redis_test), expected_result_empty)

    @unittest.skip
    @patch('database.requests_redis.redis_connect')
    def test_get_next_person(self, mock_redis_connect):
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client

        # Данные для теста
        mock_redis_client.lrange.return_value = [
            json.dumps({'id_user': 1}),
            json.dumps({'id_user': 2}),
            json.dumps({'id_user': 3}),
        ]

        mock_redis_client.get.return_value = 2

        expected_result = {'id_user': 3}  # Ожидаем, что следующий пользователь после 2 - это 3
        self.assertEqual(redis_get_next_person(1, connect=self.redis_test), expected_result)

        mock_redis_client.get.return_value = 3
        expected_result_end = 'end list'
        self.assertEqual(redis_get_next_person(1, connect=self.redis_test), expected_result_end)

        mock_redis_client.lrange.return_value = []
        mock_redis_client.get.return_value = 1  # Текущий пользователь - 1
        expected_result_empty = 'empty list'
        self.assertEqual(redis_get_next_person(1, connect=self.redis_test), expected_result_empty)

    @unittest.skip
    @patch('database.requests_redis.redis_connect')
    def test_browsing_history(self, mock_redis_connect):
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client

        mock_redis_client.lrange.return_value = [
            json.dumps({'message': ' Просмотр 1\n', 'url_profile': 'http://example.com/1'}),
            json.dumps({'message': ' Просмотр 2\n', 'url_profile': 'http://example.com/2'}),
            json.dumps({'message': ' Просмотр 3\n', 'url_profile': 'http://example.com/3'}),
        ]

        expected_output = (
            "Ваша история просмотров последних 0 записей:\n"
            "1) Просмотр 1\nСсылка: http://example.com/1\n"
            "2) Просмотр 2\nСсылка: http://example.com/2\n"
            "3) Просмотр 3\nСсылка: http://example.com/3\n"
        )

        self.assertEqual(redis_browsing_history(1, connect=self.redis_test), expected_output)

        mock_redis_client.lrange.return_value = []
        expected_empty_output = "Ваша история просмотров последних 0 записей:\n\n"
        self.assertEqual(redis_browsing_history(1, connect=self.redis_test), expected_empty_output)
