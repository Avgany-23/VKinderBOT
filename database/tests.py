from unittest import TestCase
from create_bd import create_object_db, delete_object_db, check_bd, create_bd
from sqlalchemy import create_engine, inspect
from test_settings import PATH_TEST_POSTGRESQL


class TestDatabaseCheckTablesAndCreateTables(TestCase):
    @classmethod
    def tearDownClass(cls):
        """За счет данного метода после всех тестов База данных будет удаляться"""
        delete_object_db(PATH_TEST_POSTGRESQL)

    def test_database_creation(self):
        """Тест создания базы в PostgresSQL"""
        result = create_object_db(PATH_TEST_POSTGRESQL)
        self.assertEqual(1, result[0], 'ДатаБаза не создана.')

    def test_tables_check(self):
        """Тест проверка отсутствия таблиц"""
        result = check_bd(PATH_TEST_POSTGRESQL)
        self.assertTrue(result, 'Таблицы присутствуют в ДатаБазе.')

    def test_tables_creation(self):
        """Тест создания таблиц в PostgreSQL."""
        create_bd(PATH_TEST_POSTGRESQL)
        engine = create_engine(PATH_TEST_POSTGRESQL)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        list_tables = ['users', 'likedlist', 'blacklist', 'filtersusers', 'infousers', "searchpeople"]
        for i, tab in enumerate(list_tables):
            with self.subTest(i):
                self.assertIn(tab, tables, 'Результат теста: Таблицы не созданы.')
