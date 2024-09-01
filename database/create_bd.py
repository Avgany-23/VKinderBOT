from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine
from database.models import basic
from database.requests_redis import redis_connect
import sqlalchemy


def create_object_db(path: str) -> tuple[int, None] | tuple[int, str]:
    """Создание Базы Данных по пути path"""

    for_create_path = path[:path.rfind('/')]
    for_create_db = path[path.rfind('/') + 1:]

    try:
        with sqlalchemy.create_engine(for_create_path, isolation_level='AUTOCOMMIT').connect() as connection:
            connection.execute(text(f'CREATE DATABASE {for_create_db}'))
        print(f'База данных {for_create_db} успешно создалась')
        return 1, None
    except (sqlalchemy.exc.OperationalError, UnicodeDecodeError) as e:
        return -1, e
    except sqlalchemy.exc.ProgrammingError as e:
        return -2, e


def check_bd(path_: str) -> bool:
    """Функция проверяет, существуют ли таблицы в БД. Принимает конфиг к Базе Данных - path
    Если хоть 1 таблица с именем созданных моделей будет существовать,
    то выдаст ошибку, в ином случае вернёт True"""
    engine = create_engine(path_)
    with engine.connect() as conn:
        tables = []                                         # Список существующих таблиц
        for table in basic.__subclasses__():                # проход по всем созданным моделям
            table = table.__name__.lower()                  # Получение имён моделей (таблиц из файла models.py)

            if conn.execute(text("""SELECT EXISTS
                                   (SELECT FROM information_schema.tables
                                    WHERE table_name = :table_name);"""), {'table_name': table}).scalar():
                tables.append(table)
        if tables:                                          # Если хоть одна таблица существует, то вызов исключения
            raise SystemExit(f"Таблица(ы) {', '.join(tables)} существует в указанной вами базе. "
                             f"Создание таблиц не произошло")
        return True                                         # Если ни одной таблицы не существует, то можно создавать БД


def create_bd(info_path: str) -> None:
    """Функция для создания базы данных"""
    engine = create_engine(info_path)   # Получение движка
    session = sessionmaker(engine)()    # Подключение к сессии
    basic.metadata.drop_all(engine)     # Удаление таблиц с таким же именем, если они есть
    basic.metadata.create_all(engine)   # Создание таблиц
    session.commit(), session.close()   # Коммит и закрытие сессии


def delete_object_db(path: str):
    """Удаление Базы Данных по пути path"""
    for_delete_path = path[:path.rfind('/')]
    for_delete_db = path[path.rfind('/') + 1:]

    try:
        with sqlalchemy.create_engine(for_delete_path, isolation_level='AUTOCOMMIT').connect() as connection:
            connection.execute(text(f'DROP DATABASE IF EXISTS {for_delete_db} WITH (FORCE);'))
            connection.commit()
        return 1, None
    except (sqlalchemy.exc.OperationalError, UnicodeDecodeError) as e:
        return -1, e


def create_bd_and_tables_if_not_exists():
    from database import PATH

    # --- Создание Базы Данных и таблиц в ней ---
    create_bd_ = create_object_db(PATH)     # Создание Базы данных
    if create_bd_[0] == -1:
        print('Создание Базы Данных не произошло. Неправильно указаны настройки к подключению')
        return -3
        # Тут поставить лог 3 уровня
    elif create_bd_[0] == -2:
        print(f'Созданы Базы данных не произошло. База данных с именем  {PATH[PATH.rfind("/") + 1:]}  уже существует')
    try:
        check_bd(PATH)                      # Проверка наличия таблиц в БД
    except SystemExit as e:
        print(e)
        if create_bd_[0] == 1:
            return -2
        if create_bd_[0] == -2:
            return -1
    else:

        create_bd(PATH)                     # Создание таблиц в БД
        redis_connect().flushdb()           # Если всё создано успешно, что весь кеш из Редиса очищается
        print('База данных и таблицы успешно созданы, кеш в Redis очищен.')
        return 1
        # Тут поставить лог 1 уровня
