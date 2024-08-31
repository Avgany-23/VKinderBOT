from unittest import TestCase
from test_settings import PATH_TEST_POSTGRESQL, test_UsersBd, test_InfoUsersBd, test_LikedListBD, test_BlackListBD
from ..create_bd import create_object_db, delete_object_db, create_bd

class TestUsersOperations(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание ДатаБазы, Заливка таблиц, Создать 2х юзеров"""
        create_object_db(PATH_TEST_POSTGRESQL)
        create_bd(PATH_TEST_POSTGRESQL)
        id_test_list = [100000, 2000000]
        for id_test in id_test_list:
            test_UsersBd.create_user(id_test)

    @classmethod
    def tearDownClass(cls):
        """За счет данного метода после всех тестов База данных будет удаляться"""
        delete_object_db(PATH_TEST_POSTGRESQL)

    def test_add_user(self):
        """
        Тест проверяет результат создания пользователя в функции create_user.
        Тестируемая функция create_user(id_vk)
        Пользователь не создался == -1
        Пользователь создался == 1
        """
        # result получает ответ от функции о результате создания пользователя
        id_people = [12, 10, 9, 8, 11, 20]
        for i, id_vk in enumerate(id_people):
            with self.subTest(i):
                result = test_UsersBd.create_user(id_vk)
                expected = 1
                self.assertEqual(expected, result, 'Результат теста: Пользователь не создался.')

    def test_delete_user(self):
        """Тест проверяет работу функции delete_user"""
        dell_id_people = [12, 10, 9, 8, 11, 20]
        for i, id_vk in enumerate(dell_id_people):
            with self.subTest(i):
                result = test_UsersBd.delete_user(id_vk)
                expected = 1
                self.assertEqual(expected, result, 'Результат теста: Пользователь не удалён.')

    def test_update_user_id(self):
        """Тест проверяет работу функции  update_user_id
        """
        id_test_user_old = 100000
        id_test_user_new = 100001
        result = test_UsersBd.update_user_id(id_test_user_old, id_test_user_new)
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: ID пользователя не изменён.')

    def test_get_one_user(self):
        """Тест проверяет работу функции get_one_user, которая возвращает
        информацию о пользователю по vk_id
        """
        id_test_user = 2000000
        result = test_UsersBd.get_one_user(id_test_user)
        # тест сравнивает id из запроса с id из ответа
        self.assertIsNotNone(result, 'Результат теста: Информация по ID не загружено.')

    def test_info_users(self):
        """Тест проверяет работу функции info_users
        Функция загружает информацию о пользователе"""
        id_test_user = 2000000
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
        result = test_InfoUsersBd.add_info_users(id_test_user, **kwargs)
        # Успешная загрузка информации == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')

    def test_add_like_user(self):
        """Тест проверяет работу функции add_like_user
        Функция добавляет ID пользователя в Like"""
        id_test_user = 2000000
        id_test_like = 1
        name_people = "Вася"
        result = test_LikedListBD.add_like_user(id_test_user, id_test_like, name_people)
        # Успешная загрузка информации == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')

    def test_get_like_user(self):
        """Тест проверяет работу функции get_like_user
        функция получает информацию о наличии ID в Like"""
        id_test_user = 2000000
        id_test_like = 1
        result = test_LikedListBD.get_like_user(id_test_user, id_test_like)
        # Успешная загрузка информации == 1

        self.assertIsNotNone(result, 'Результат теста: Информация о пользователе не получена.')

    def test_dell_like_user(self):
        """Тест проверяет работу функцию dell_like_user
        удаляет ранее созданной связки ID пользователя + ID понравившегося пользователя"""
        id_test_user = 2000000
        id_test_like = 1
        result = test_LikedListBD.delete_like_user(id_test_user, id_test_like)
        # Успешная загрузка информации == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не Удалена.')

    def test_add_black_list(self):
        """Тест проверяет работу функцию add_black_list
        Функция добавляет пользователю в black list ID блокируемого пользователя"""
        id_test_user = 2000000
        id_test_like = 2
        name_people = "Вася"
        result = test_BlackListBD.add_user_black_list(id_test_user, id_test_like, name_people)
        # Успешная операция == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')

    def test_get_black_list(self):
        """Тест проверяет работу функции get_like_user
        получить информацию о наличии блокировки по ID"""
        id_test_user = 2000000
        result = test_BlackListBD.get_all_users(id_test_user)
        self.assertIsNotNone(result, 'Результат теста: Информация о пользователе не получена.')

    def test_dell_black_list(self):
        """Тест проверяет работу функцию dell_black_list
        Функция удаляет из списка пользователя конкретный ID"""
        id_test_user = 2000000
        id_test_like = 2
        result =test_BlackListBD.delete_user_black_list(id_test_user, id_test_like)
        # Успешная операция
        expected = 1
        # Обработка return с ошибкой.
        if result == 1:
            self.assertEqual(expected, result)
        else:
            #Ошибка лежит в result[1]
            self.assertEqual(expected, result[0], 'Результат теста: Информация о пользователе не Удалена.')