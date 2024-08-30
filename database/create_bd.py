from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine
from database import PATH
from models import basic
import sqlalchemy


def create_object_db(path: str) -> tuple[int, None] | tuple[int, str]:
    """Создание Базы Данных по пути path"""

    for_create_path = path[:path.rfind('/')]
    for_create_db = path[path.rfind('/') + 1:]

    try:
        with sqlalchemy.create_engine(for_create_path, isolation_level='AUTOCOMMIT').connect() as connection:
            connection.execute(text(f'CREATE DATABASE {for_create_db}'))
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

            raise SystemExit(f"Таблица(ы) {', '.join(tables)} существует в указанной вами базе.\n"
                             f"Создание таблиц не произошло")
        return True                                         # Если ни одной таблицы не существует, то можно создавать БД


def create_bd(info_path: str) -> None:
    """Функция для создания базы данных"""
    engine = create_engine(info_path)               # Получение движка
    with sessionmaker(bind=engine)() as session:    # Подключение к сессии
        basic.metadata.drop_all(engine)             # Удаление таблиц с таким же именем, если они есть
        basic.metadata.create_all(engine)           # Создание таблиц
        session.commit()                            # Коммит
        print('БД успешна создана')                 # Оповещение об успешном создании БД


def delete_object_db(path: str):
    """Удаление Базы Данных по пути path"""
    for_delete_path = path[:path.rfind('/')]
    for_delete_db = path[path.rfind('/') + 1:]

    try:
        with sqlalchemy.create_engine(for_delete_path, isolation_level='AUTOCOMMIT').connect() as connection:
            connection.execute(text(f'DROP DATABASE IF EXISTS {for_delete_db}'))
        return 1, None
    except (sqlalchemy.exc.OperationalError, UnicodeDecodeError) as e:
        return -1, e



if __name__ == '__main__':
    # --- Создание Базы Данных и таблиц в ней ---
    create_bd_ = create_object_db(PATH)
    if create_bd_[0] == -1:
        print('Создание Базы Данных не произошло. Неправильно указаны настройки к подключению')
    elif create_bd_[0] == -2:
        print('Созданы Базы данных не произошло. База данных с таким именем уже существует')
    if check_bd(PATH):
        create_bd(PATH)   # Создание БД
        print('База данных и таблицы успешно созданы')