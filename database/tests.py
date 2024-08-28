from unittest import TestCase
from create_bd import create_object_db, check_bd, create_bd
from sqlalchemy import create_engine, inspect
from notification import PATH

class Test_database_check_tables_and_create_tables(TestCase):
    def test_database_creation(self):
        """Тест создания базы в PostgresSQL"""
        # result получает ответ от функции create_object_db о результате создания ДатаБазы
        result = create_object_db(PATH)
        # ДБ создана == 1. Принято положительным исходом
        expected = 1
        self.assertEqual(expected, result, 'Результат теста: ДатаБаза не создана.')


    def test_tables_check(self):
        """Тест проверка отсутсвия таблиц"""
        # result получает ответ от функции check_bd о результатах проверки наличия Таблиц
        result = check_bd(PATH)
        # Таблицы созданы == True. Принято положительным исходом
        expected = True
        self.assertEqual(expected, result, 'Результат теста: Таблицы не созданы.')


    def test_tables_creation(self):
        """Тест создания таблиц в PostgreSQL."""
        create_bd(PATH)
        engine = create_engine(PATH)
        # Проверяем, существует ли таблица 'users'
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        list_tables = ['users', 'likedlist', 'blacklist', 'filtersusers', 'infousers', "searchpeople"]
        for i, tab in enumerate(list_tables):
            with self.subTest(i):
                self.assertIn(tab, tables, 'Результат теста: Таблицы не созданы.')

