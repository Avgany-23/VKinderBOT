from unittest import TestCase
from users import UsersBd
from info_users import InfoUsersBd
"""Тестирование создание пользователя"""

# Создаем экземпляр класса UsersBd
users_bd = UsersBd()
info_users_bd = InfoUsersBd()
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
        """Тест проверяет работу функции info_users"""
        result = info_users_bd.info_users(id_user, name, age, gender, marital_status, city, interests)
        # Успешная загрузка информации == 1
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')


