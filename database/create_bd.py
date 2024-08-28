import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine
from models import basic
from settings import DATABASES

def create_object_db(path: str):
    """Создаём ДАТА БАЗУ для заливки в неё Таблиц согласно моделям"""
    for_create_path = path[:-path.find("/")+3:]         # получаем путь для подклюния
    for_create_db = path[-path.find("/") + 4::]         # получаем имя Базы Данных
    try:
        with sqlalchemy.create_engine(for_create_path,
        isolation_level='AUTOCOMMIT').connect() as connection:
            connection.execute(text(f'CREATE DATABASE {for_create_db}'))
        return 1
    except:
        return -1
def check_bd(path: str) -> bool:
    """Функция проверяет, существуют ли таблицы в БД. Принимает конфиг к Базе Данных - path
    Если хоть 1 таблица с именем созданных моделей будет существовать,
    то выдаст ошибку, в ином случае вернёт True"""
    engine = create_engine(path)
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


if __name__ == '__main__':
    # --- Получение данных о Базе Данных (название, логин, пароль) ---
    data_bd = DATABASES['postgresql']
    path = (f"{data_bd['NAME']}://{data_bd['USER']}:{data_bd['PASSWORD']}@"
            f"{data_bd['HOST']}:{data_bd['PORT']}/{data_bd['BD_NAME']}")


    # --- Если ни одной таблицы в БД с названием моделей не существует, то создается новая база данных ---
    create_object_db(path)
    if check_bd(path):
        create_bd(path)  # Создание БД

