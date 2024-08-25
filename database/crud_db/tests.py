from unittest import TestCase
from users import UsersBd
from info_users import InfoUsersBd
from liked_list import LikedListBb
from black_list import BlackListBd
"""Тестирование создание пользователя"""

# Создаем экземпляры классов
users_bd = UsersBd()
info_users_bd = InfoUsersBd()
liked_list_bd = LikedListBb()
black_list_bd = BlackListBd()
#Test_add_dell_user
id_vk = 1000001
old_id = 1000000
new_id = 2000000
test_one_id = 1234537
#Test_info_user
id_user = 1234537
name = "Ловелас"
age = 21
gender = "мужской"
marital_status = "активный поиск"
city = "Москва"
interests = "Музыка"
#Test_liked_list
id_user = 1234537
id_like_user = 999
#Test_black_list
id_user = 1234537
id_ignore_user = 888

class Test_users_operations(TestCase):
    def test_add_user(self):
        """Тест проверяет результат создания пользователя в функции create_user.
        Тестируемая функция create_user(id_vk)
        Пользователь не создался == -1
        Пользователь создался == 1
        """
        # result получает ответ от функции о результате создания пользователя
        result = users_bd.create_user(id_vk)
        # Пользователь создался == 1. Принято положительным исходом
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Пользователь не создался.')


    def test_delete_user(self):
        """Тест проверяет работу функции delete_user
         удаляет тестового юзера созданного в проверке test_registration
        """
        # result получает ответ от функции о результате удаления пользователя
        result = users_bd.delete_user(id_vk)
        # Пользователь удалён == 1. Принято положительным исходом
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Пользователь не удалён.')


    def test_update_user_id(self):
        """Тест проверяет работу функции  update_user_id
        """
        # result получает ответ от функции о результатах замены
        result = users_bd.update_user_id(old_id, new_id)
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: ID пользователя не изменён.')


    def test_get_one_user(self):
        """Тест проверяет работу функции get_one_user, которая возвращает
        информацию о пользователю по vk_id
        """
        # result получает ответ от функции с данными пользователя
        result = users_bd.get_one_user(test_one_id)
        expected = test_one_id
        # тест сравнивает id из запроса с id из ответа
        self.assertEqual(expected, result[0], 'Результат теста: Информация по ID не загружено.')

class Test_info_users(TestCase):
    def test_info_users(self):
        """Тест проверяет работу функции info_users
        Функция загружает информацию о пользователе"""
        result = info_users_bd.info_users(id_user, name, age, gender, marital_status, city, interests)
        # Успешная загрузка информации == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')


class Test_liked_list(TestCase):

    def test_add_like_user(self):
        """Тест проверяет работу функции add_like_user
        Функция добавляет ID пользователя в Like"""
        result = liked_list_bd.add_like_user(id_user, id_like_user)
        # Успешная загрузка информации == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')


    def test_get_like_user(self):
        """Тест проверяет работу функции get_like_user
        функция получает информацию о наличии ID в Like"""
        result = liked_list_bd.get_like_user(id_user, id_like_user)
        # Успешная загрузка информации == 1
        expected = id_like_user
        self.assertEqual(expected, result[1], 'Результат теста: Информация о пользователе не получена.')


class Test_liked_list2(TestCase):
    def test_dell_like_user(self):
        """Тест проверяет работу функцию dell_like_user
        удаляет ранее созданной связки ID пользователя + ID понравившегося пользователя"""

        result = liked_list_bd.dell_like_user(id_user, id_like_user)
        # Успешная загрузка информации == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не Удалена.')


class Test_black_list(TestCase):
    def test_add_black_list(self):
        """Тест проверяет работу функцию add_black_list
        Функция добавляет пользователю в black list ID блокируемого пользователя"""
        result = black_list_bd.add_black_list(id_user, id_ignore_user)
        # Успешная операция == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')


    def test_get_black_list(self):
        """Тест проверяет работу функции get_like_user
        получить информацию о наличии блокировки по ID"""
        result = black_list_bd.get_black_list(id_user, id_ignore_user)
        # Успешная загрузка информации == 1
        expected = id_ignore_user

        self.assertEqual(expected, result[1], 'Результат теста: Информация о пользователе не получена.')


class Test_black_list2(TestCase):
    def test_dell_black_list(self):
        """Тест проверяет работу функцию dell_black_list
        Функция удаляет из списка пользователя конкретный ID"""
        result = black_list_bd.dell_black_list(id_user, id_ignore_user)
        # Успешная операция
        expected = 1
        # Обработка return с ошибкой.
        if result == 1:
            self.assertEqual(expected, result)
        else:
            #Ошибка лежит в result[1]
            self.assertEqual(expected, result[0], 'Результат теста: Информация о пользователе не Удалена.')