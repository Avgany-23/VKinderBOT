# from unittest import TestCase
# from notification import users_bd, id_vk, old_id, new_id, test_one_id, info_users_bd, id_user
# from notification import liked_list_bd, id_like_user, black_list_bd, kwargs
# from notification import id_ignore_user
#
#
# class TestUsersOperations(TestCase):
#     def SetUpModule(self):
#         # Сработает перед запуском всех тестов, тут можно создать БД, где будут проводиться тесты.
#         ...
#
#     def TearDownModule(self):
#         # Сработает в конце всех тестов, тут надо записать удаление БД
#         ...
#
#     def test_add_user(self):
#         """
#         Тест проверяет результат создания пользователя в функции create_user.
#         Тестируемая функция create_user(id_vk)
#         Пользователь не создался == -1
#         Пользователь создался == 1
#         """
#         # result получает ответ от функции о результате создания пользователя
#         result = users_bd.create_user(id_vk)
#         # Пользователь создался == 1. Принято положительным исходом
#         expected = 1
#         self.assertEqual(expected, result, 'Результат теста: Пользователь не создался.')
#
#     def test_delete_user(self):
#         """Тест проверяет работу функции delete_user
#          удаляет тестового юзера созданного в проверке test_registration
#         """
#         # result получает ответ от функции о результате удаления пользователя
#         result = users_bd.delete_user(id_vk)
#         # Пользователь удалён == 1. Принято положительным исходом
#         expected = 1
#         self.assertEqual(expected, result, 'Результат теста: Пользователь не удалён.')
#
#     def test_update_user_id(self):
#         """Тест проверяет работу функции  update_user_id
#         """
#         # result получает ответ от функции о результатах замены
#         result = users_bd.update_user_id(old_id, new_id)
#         expected = 1
#         self.assertEqual(expected, result, 'Результат теста: ID пользователя не изменён.')
#
#     def test_get_one_user(self):
#         """Тест проверяет работу функции get_one_user, которая возвращает
#         информацию о пользователю по vk_id
#         """
#         # result получает ответ от функции с данными пользователя
#         result = users_bd.get_one_user(test_one_id)
#         # тест сравнивает id из запроса с id из ответа
#         self.assertIsNotNone(result, 'Результат теста: Информация по ID не загружено.')
#
#
# class TestInfoUsers(TestCase):
#     def test_info_users(self):
#         """Тест проверяет работу функции info_users
#         Функция загружает информацию о пользователе"""
#         result = info_users_bd.add_info_users(id_user, **kwargs)
#         # Успешная загрузка информации == 1
#         expected = 1
#         self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')
#
#
# class TestLikedList(TestCase):
#     def test_add_like_user(self):
#         """Тест проверяет работу функции add_like_user
#         Функция добавляет ID пользователя в Like"""
#         result = liked_list_bd.add_like_user(id_user, id_like_user)
#         # Успешная загрузка информации == 1
#         expected = 1
#         self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')
#
#     def test_get_like_user(self):
#         """Тест проверяет работу функции get_like_user
#         функция получает информацию о наличии ID в Like"""
#         result = liked_list_bd.get_like_user(id_user, id_like_user)
#         # Успешная загрузка информации == 1
#
#         self.assertIsNotNone(result, 'Результат теста: Информация о пользователе не получена.')
#
#
# class TestLikedList2(TestCase):
#     def test_dell_like_user(self):
#         """Тест проверяет работу функцию dell_like_user
#         удаляет ранее созданной связки ID пользователя + ID понравившегося пользователя"""
#
#         result = liked_list_bd.delete_like_user(id_user, id_like_user)
#         # Успешная загрузка информации == 1
#         expected = 1
#         self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не Удалена.')
#
#
# class TestBlackList(TestCase):
#     def test_add_black_list(self):
#         """Тест проверяет работу функцию add_black_list
#         Функция добавляет пользователю в black list ID блокируемого пользователя"""
#         result = black_list_bd.add_user_black_list(id_user, id_ignore_user)
#         # Успешная операция == 1
#         expected = 1
#         self.assertEqual(expected, result, 'Результат теста: Информация о пользователе не загружена.')
#
#     def test_get_black_list(self):
#         """Тест проверяет работу функции get_like_user
#         получить информацию о наличии блокировки по ID"""
#         result = black_list_bd.get_all_users(id_user)
#         self.assertIsNotNone(result, 'Результат теста: Информация о пользователе не получена.')
#
#
# class TestBlackList2(TestCase):
#     def test_dell_black_list(self):
#         """Тест проверяет работу функцию dell_black_list
#         Функция удаляет из списка пользователя конкретный ID"""
#         result = black_list_bd.delete_user_black_list(id_user, id_ignore_user)
#         # Успешная операция
#         expected = 1
#         # Обработка return с ошибкой.
#         if result == 1:
#             self.assertEqual(expected, result)
#         else:
#             #Ошибка лежит в result[1]
#             self.assertEqual(expected, result[0], 'Результат теста: Информация о пользователе не Удалена.')