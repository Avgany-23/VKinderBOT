from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine
from models import basic
from settings import DATABASES


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
    engine = create_engine(info_path)   # Получение движка
    session = sessionmaker(engine)()    # Подключение к сессии
    basic.metadata.drop_all(engine)     # Удаление таблиц с таким же именем, если они есть
    basic.metadata.create_all(engine)   # Создание таблиц
    print('БД успешна создана')         # Оповещение об успешном создании БД
    session.commit(), session.close()   # Коммит и закрытие сессии


if __name__ == '__main__':
    # --- Получение данных о Базе Данных (название, логин, пароль) ---
    data_bd = DATABASES['postgresql']
    path = (f"{data_bd['NAME']}://{data_bd['USER']}:{data_bd['PASSWORD']}@"
            f"{data_bd['HOST']}:{data_bd['PORT']}/{data_bd['BD_NAME']}")

    # --- Если ни одной таблицы в БД с названием моделей не существует, то создается новая база данных ---
    if check_bd(path):
        create_bd(path)  # Создание БД