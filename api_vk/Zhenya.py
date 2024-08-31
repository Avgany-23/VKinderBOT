from unittest import TestCase
import logging
from requests_redis import redis_connect, redis_set_person, redis_set_current_person, redis_get_person_info, redis_get_current_person, redis_person_is_current, redis_person_is_last, redis_get_prev_person, redis_get_next_person, redis_clear_user_id, redis_save_history, redis_browsing_history
import json
import unittest
from unittest.mock import patch, MagicMock


#Настройка пользовательского логгера
logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)

# настройка обработчика и форматировщика для logger2
handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler2.setFormatter(formatter2)
# добавление обработчика к логгеру
logger2.addHandler(handler2)

logger2.info(f"Testing the custom logger for module {__name__}...")
def redis_connect_test() -> tuple[str, ConnectionError] | Redis:
    """Подключение к редису"""
    redis_data = DATABASES_TEST['redis']
    try:
        connect = redis.StrictRedis(host=redis_data['host'],
                                    port=redis_data['port'],
                                    db=redis_data['db'],
                                    decode_responses=redis_data['decode_responses'],
                                    encoding=redis_data['charset'])
    except redis.exceptions.ConnectionError as e:
        return 'Ошибка при подключении к Redis', e
    return connect

class TestRedis_func(TestCase):

    def setUp(self):
        # Подключаемся к Redis и очищаем базу данных перед каждым тестом
        self.redis_test = redis_connect(DATABASES_TEST['redis'], charset_=False)
        self.redis_test.flushdb()  # Очищаем базу данных

    def tearDown(self):
        # Очистка базы данных после теста
        self.redis_test.flushdb()

    def test_redis_connect(self):
        try:
            result = redis_connect()
            expected = 'redis.connection.ConnectionPool'
            self.assertIn(expected, str(result))
            logger2.info(f'successful with result: {result}.')
        except KeyError as err:
            logger2.exception(f'check if the fields are filled in "connect" {err}')
        except TypeError as err:
            logger2.exception(f'check the arguments {err}')
        except AttributeError as err:
            logger2.exception(f'check the attribute module "redis" {err}')

    def test_redis_set_person(self):
        id_user = 5
        message = {"one": "two"}
        redis_set_person(id_user, message)
        # Проверка, что сообщение записано
        key = f"search_{id_user}"
        result = connect=self.redis_test.lrange(key, 0, -1)
        self.assertEqual(len(result), 1)
        self.assertEqual(json.loads(result[0]), message)
        logger2.info(f'successful')

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
            redis_set_person(id_user, message)
        # Проверяем, что в списке осталось только 3 сообщения
        key = f"search_{id_user}"
        result = self.redis_test.lrange(key, 0, -1) #метод lrange получить элементы из списка под определенным ключом от 0 до -1(от начала д конца)
        self.assertEqual(len(result), 3)
        # Проверяем, что самое старое сообщение было удалено
        expected_messages = [{"g4": "z4"}, {"e3": "f3"}, {"c2": "d2"}]
        self.assertEqual([json.loads(msg) for msg in result], expected_messages)
        logger2.info(f'successful')

    def test_redis_set_current_person(self):
        user_id = 1
        id_search_user = 42
        redis_set_current_person(user_id, id_search_user)
        # Проверяем, что значение установлено верно
        result = self.redis_test.get(f'current_person_{user_id}')
        self.assertIsNotNone(result)
        self.assertEqual(int(result), id_search_user)
        logger2.info(f'successful')

    def test_redis_get_current_person(self):
        user_id = 1
        id_search_user = 12
        #нам надо установить значения через функцию redis_set_current_person
        redis_set_current_person(user_id, id_search_user)
        result = redis_get_current_person(user_id)
        # Проверяем
        self.assertIsNotNone(result)
        self.assertEqual(int(result), id_search_user)
        logger2.info(f'successful')

    def test_redis_get_person_info(self):
        user_id = 9
        test_data = [
            {"name": "Пользователь Катя", "age": 30, "url_profile": "http://example.com/userКатя"},
            {"name": "Пользователь Оля", "age": 25, "url_profile": "http://example.com/userОля"},
            {"name": "Пользователь Cережа", "age": 28, "url_profile": "http://example.com/userСережа"},
        ]
        for item in test_data:
            self.redis_test.rpush(f"search_{user_id}", json.dumps(item)) #rpush добавление одного или нескольких элементов в конец списка.
        result = redis_get_person_info(user_id)
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
        redis_clear_user_id(user_id)
        # Проверка  удаления
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
            redis_save_history(user_id, messages[i])
        # Добавляем 7-е сообщение, что должно вызвать удаление
        redis_save_history(user_id, messages[6])
        # Получаем историю из Redis
        history = [json.loads(msg) for msg in self.redis_test.lrange(f'history_{user_id}', 0, -1)]
        # Проверка, что в истории остались только последние 6 сообщений
        self.assertEqual(len(history), 6)  # Должно быть 6 сообщений
        self.assertEqual(history[0]['text'], "message 7")  # Проверяем, что последнее сообщение - "message 7"
        self.assertEqual(history[-1]['text'], "message 2")  # Проверяем, что первое сообщение в истории - "message 2"

    @patch('requests_redis.redis_get_current_person')
    @patch('requests_redis.redis_connect')
    def test_redis_person_is_current(self, mock_redis_connect, mock_redis_get_current_person):
        # Настройка mock для Redis
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client
        # Настройка возвращаемых значений для lrange
        mock_redis_client.lrange.return_value = [
            json.dumps({'id_user': 1}),
            json.dumps({'id_user': 2}),
            json.dumps({'id_user': 3}),
        ]
        try:
            # Установка текущей анкеты
            mock_redis_get_current_person.return_value = 3
            # Проверка, что функция возвращает True, когда последняя анкета совпадает
            self.assertTrue(redis_person_is_current(1))
            # Изменение текущей анкеты
            mock_redis_get_current_person.return_value = 2
            # Проверка, что функция возвращает False, когда последняя анкета не совпадает
            self.assertFalse(redis_person_is_current(1))
            # Тест на случай, когда lrange возвращает пустой список
            mock_redis_client.lrange.return_value = []
            mock_redis_get_current_person.return_value = 1
            # Проверка, что функция возвращает True, когда нет анкеты
            self.assertTrue(redis_person_is_current(1))
            # Печать всех вызовов для проверки
            logger2.info(f'successful {mock_redis_client.lrange.call_args_list}')
        except IndexError as er:
            logger2.exception(f'check the database, maybe there are no entries there {er}')

    @patch('requests_redis.redis_get_current_person')
    @patch('requests_redis.redis_connect')
    def test_person_is_last(self, mock_redis_connect, mock_redis_get_current_person):
        # Настройка mock для Redis
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client
        # Подготовка данных, которые будут возвращаться от lrange
        mock_redis_client.lrange.return_value = [
            json.dumps({'id_user': 1}),
            json.dumps({'id_user': 2}),
            json.dumps({'id_user': 3}),
        ]
        # Настройка текущей анкеты
        mock_redis_get_current_person.return_value = 3
        # Проверка, что функция возвращает True, когда текущая анкета совпадает
        self.assertTrue(redis_person_is_last(1))
        # Изменение текущей анкеты
        mock_redis_get_current_person.return_value = 2
        # Проверка, что функция возвращает False, когда текущая анкета не совпадает
        self.assertFalse(redis_person_is_last(1))
        # Тест на случай, когда lrange возвращает пустой список
        mock_redis_client.lrange.return_value = []
        # Проверка на работу функции в случае пустого списка. Это должно вызвать IndexError,
        # поэтому мы обернем в assertRaises
        with self.assertRaises(IndexError):
            redis_person_is_last(1)
        # Дополнительно, тестируем случай, когда только одна анкета
        mock_redis_client.lrange.return_value = [
            json.dumps({'id_user': 1}),
        ]
        mock_redis_get_current_person.return_value = 1
        # Проверка с единственной анкетой
        self.assertTrue(redis_person_is_last(1))

    @unittest.skip
    @patch('requests_redis.redis_connect')
    def test_get_prev_person(self, mock_redis_connect):
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client

        # Данные для теста
        mock_redis_client.lrange.return_value = [
            json.dumps({'id_user': 1}),
            json.dumps({'id_user': 2}),
            json.dumps({'id_user': 3}),
        ]

        # Текущий пользователь 2
        mock_redis_client.get.return_value = 2

        # Проверяем, возвращается ли правильный предыдущий пользователь
        expected_result = {'id_user': 1}
        self.assertEqual(redis_get_prev_person(1), expected_result)

        # Текущий пользователь 3 (последний в списке)
        mock_redis_client.get.return_value = 3
        expected_result_end = 'end list'
        self.assertEqual(redis_get_prev_person(1), expected_result_end)

        # Проверка на случай, когда список пустой
        mock_redis_client.lrange.return_value = []
        mock_redis_client.get.return_value = 1
        expected_result_empty = 'empty list'
        self.assertEqual(redis_get_prev_person(1), expected_result_empty)

    @unittest.skip
    @patch('requests_redis.redis_connect')
    def test_get_next_person(self, mock_redis_connect):
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client

        # Данные для теста
        mock_redis_client.lrange.return_value = [
            json.dumps({'id_user': 1}),
            json.dumps({'id_user': 2}),
            json.dumps({'id_user': 3}),
        ]

        # Текущий пользователь 2
        mock_redis_client.get.return_value = 2

        # Проверяем, возвращается ли правильный следующий пользователь
        expected_result = {'id_user': 3}  # Ожидаем, что следующий пользователь после 2 - это 3
        self.assertEqual(redis_get_next_person(1), expected_result)

        # Текущий пользователь 3 (последний в списке)
        mock_redis_client.get.return_value = 3
        expected_result_end = 'end list'
        self.assertEqual(redis_get_next_person(1), expected_result_end)

        # Проверка на случай, когда список пустой
        mock_redis_client.lrange.return_value = []
        mock_redis_client.get.return_value = 1  # Текущий пользователь - 1
        expected_result_empty = 'empty list'
        self.assertEqual(redis_get_next_person(1), expected_result_empty)

    @unittest.skip
    @patch('requests_redis.redis_connect')
    def test_browsing_history(self, mock_redis_connect):
        mock_redis_client = MagicMock()
        mock_redis_connect.return_value = mock_redis_client

        # Данные для теста
        mock_redis_client.lrange.return_value = [
            json.dumps({'message': ' Просмотр 1\n', 'url_profile': 'http://example.com/1'}),
            json.dumps({'message': ' Просмотр 2\n', 'url_profile': 'http://example.com/2'}),
            json.dumps({'message': ' Просмотр 3\n', 'url_profile': 'http://example.com/3'}),
        ]

        expected_output = (
            "Ваша история просмотров последних 3 записей:\n"
            "1) Просмотр 1\nСсылка: http://example.com/1\n"
            "2) Просмотр 2\nСсылка: http://example.com/2\n"
            "3) Просмотр 3\nСсылка: http://example.com/3\n"
        )

        self.assertEqual(redis_browsing_history(1), expected_output)

        # Проверка на случай, если истории нет
        mock_redis_client.lrange.return_value = []
        expected_empty_output = "Ваша история просмотров последних 0 записей:\n\n"
        self.assertEqual(redis_browsing_history(1), expected_empty_output)