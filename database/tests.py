# from unittest import TestCase
# from create_bd import create_object_db, check_bd, create_bd
# from sqlalchemy import create_engine, inspect
# from test_settings import PATH_TEST_POSTGRESQL
#
#
# class TestDatabaseCheckTablesAndCreateTables(TestCase):
#
#     def setUp(self):
#         # За счет данного метода перед каждым тестом будет создавать База данных
#         create_object_db(PATH_TEST_POSTGRESQL)
#
#     def TearDown(self):
#         # За счет данного метода после каждого теста База данных будет удаляться
#         # Тут вызвать удаление Базы данных. То есть в create_db написать скрипт по удалению БД
#         print('Бд удалена')
#
#     def test_database_creation(self):
#         """Тест создания базы в PostgresSQL"""
#
#         # После успешного выполнения нужно удалить созданную БД через скрипт,
#         # так как второй раз тест покажет ошибку, ведь БД уже будет создана, если не удалить её в ручную из postgresql
#
#         # Чтобы тест отработал корректно, нужно сначала удалить созданную БД (которая создается за счет setUp),
#         # а потом уже создавать БД. После теста за счет TearDown БД автоматически удалится.
#         # Подобная логика и в остальных тестах
#
#         result = create_object_db(PATH_TEST_POSTGRESQL)
#         self.assertEqual(1, result[0], 'ДатаБаза не создана.')
#
#     def test_tables_check(self):
#         """Тест проверка отсутствия таблиц"""
#
#         result = check_bd(PATH_TEST_POSTGRESQL)
#         self.assertTrue(result, 'Таблицы не созданы.')
#         check_bd(PATH_TEST_POSTGRESQL)
#         self.assertRaises(SystemExit)
#
#     def test_tables_creation(self):
#         """Тест создания таблиц в PostgreSQL."""
#         create_bd(PATH_TEST_POSTGRESQL)
#         engine = create_engine(PATH_TEST_POSTGRESQL)
#         inspector = inspect(engine)
#         tables = inspector.get_table_names()
#         list_tables = ['users', 'likedlist', 'blacklist', 'filtersusers', 'infousers', "searchpeople"]
#         for i, tab in enumerate(list_tables):
#             with self.subTest(i):
#                 self.assertIn(tab, tables, 'Результат теста: Таблицы не созданы.')
