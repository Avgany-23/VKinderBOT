from test_settings import PATH_TEST_POSTGRESQL, test_UsersBd, test_InfoUsersBd, test_LikedListBD, test_BlackListBD
from ..create_bd import create_object_db, delete_object_db, create_bd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import basic
from unittest import TestCase


class TestUsersOperations(TestCase):
    engine = create_engine(PATH_TEST_POSTGRESQL)

    @classmethod
    def setUpClass(cls):
        """Создание ДатаБазы, Заливка таблиц, Создать 2х юзеров"""
        create_object_db(PATH_TEST_POSTGRESQL)
        create_bd(PATH_TEST_POSTGRESQL)

    @classmethod
    def tearDownClass(cls):
        """За счет данного метода после всех тестов База данных будет удаляться"""
        delete_object_db(PATH_TEST_POSTGRESQL)

    def setUp(self):
        id_test_list = [100000, 2000000]
        for id_test in id_test_list:
            test_UsersBd.create_user(id_test)

    def tearDown(self):
        metadata = basic().metadata
        with sessionmaker(bind=self.engine)() as session:
            for table in reversed(metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()

    def test_add_user(self):
        """Тест проверяет результат создания пользователя в функции create_user."""
        id_people = [12, 10, 9, 8, 11, 20]
        for i, id_vk in enumerate(id_people):
            with self.subTest(i):
                result = test_UsersBd.create_user(id_vk)
                self.assertEqual(1, result, 'Результат теста: Пользователь не создался.')

    def test_delete_user(self):
        """Тест проверяет работу функции delete_user"""
        for id_ in range(1, 11):
            with self.subTest(id_):
                result = test_UsersBd.delete_user(id_)
                expected = 1
                self.assertEqual(expected, result, 'Результат теста: Пользователь не удалён.')

    def test_update_user_id(self):
        """Тест проверяет работу функции  update_user_id"""
        id_test_user_old = 100000
        id_test_user_new = 100001
        result = test_UsersBd.update_user_id(id_test_user_old, id_test_user_new)
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: ID пользователя не изменён.')

    def test_get_one_user(self):
        """Тест проверяет работу функции get_one_user, которая возвращает информацию о пользователе по vk_id"""
        id_test_user = 2000000
        result = test_UsersBd.get_one_user(id_test_user)
        self.assertIsNotNone(result, 'Результат теста: Информация по ID не загружена.')

    def test_info_users(self):
        """Тест проверяет работу функции info_users. Функция загружает информацию о пользователе"""
        kwargs = {"first_name": "Ловелас",
                  "last_name": "Донжуанович",
                  "screen_name": "Твоя мечта",
                  "sex": "2",
                  "can_access_closed": True,
                  "is_closed": False,
                  "bdate": "12.12.2024",
                  "city_id": 3,
                  "city_title": "Секретный",
                  "interests": "Python",
                  "about": "Я питонист",
                  "activities": "Тест",
                  "music": "Шифутинский",
                  "relation": 1}
        result = test_InfoUsersBd.add_info_users(2000000, **kwargs)
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')

    def test_add_like_user(self):
        """Тест проверяет работу функции add_like_user. Функция добавляет ID пользователя в Like"""
        result = test_LikedListBD.add_like_user(2000000, 1, "Вася")
        self.assertEqual(1, result, 'Результат теста: Информация о пользователе не загружена.')

    def test_get_like_user(self):
        """Тест проверяет работу функции get_like_user функция получает информацию о наличии ID в Like"""
        test_LikedListBD.add_like_user(2000000, 1, "Вася")
        result = test_LikedListBD.get_like_user(2000000, 1)
        self.assertIsNotNone(result, 'Результат теста: Информация о пользователе не получена.')

    def test_dell_like_user(self):
        """
        Тест проверяет работу функцию dell_like_user удаляет ранее созданной
        связки ID пользователя + ID понравившегося пользователя
        """
        test_LikedListBD.add_like_user(2000000, 1, "Вася")
        result = test_LikedListBD.delete_like_user(2000000, 1)
        self.assertEqual(1, result, 'Результат теста: Информация о пользователе не Удалена.')

    def test_add_black_list(self):
        """
        Тест проверяет работу функцию add_black_list.
        Функция добавляет пользователю в black list ID блокируемого пользователя
        """
        result = test_BlackListBD.add_user_black_list(2000000, 2, "Вася")
        self.assertEqual(1, result, 'Результат теста: Информация о пользователе не загружена.')

    def test_get_black_list(self):
        """Тест проверяет работу функции get_like_user получить информацию о наличии блокировки по ID"""
        test_BlackListBD.add_user_black_list(2000000, 2, "Вася")
        result = test_BlackListBD.get_all_users(2000000)
        result_ = result if result else None
        self.assertIsNotNone(result_, 'Результат теста: Информация о пользователе не получена.')

    def test_dell_black_list(self):
        """Тест проверяет работу функцию dell_black_list. Функция удаляет из списка пользователя конкретный ID"""
        result = test_BlackListBD.delete_user_black_list(2000000, 2)
        expected = 1
        if result == 1:
            self.assertEqual(expected, result)
        else:
            self.assertEqual(expected, result[0], 'Результат теста: Информация о пользователе не Удалена.')
