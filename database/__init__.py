from settings import DATABASES
from sqlalchemy.orm import sessionmaker
import sqlalchemy


data_bd = DATABASES['postgresql']
PATH = (f"{data_bd['NAME']}://{data_bd['USER']}:{data_bd['PASSWORD']}@"
        f"{data_bd['HOST']}:{data_bd['PORT']}/{data_bd['BD_NAME']}")


def session_bd(path: str) -> sessionmaker:
    engine = sqlalchemy.create_engine(path)
    return sessionmaker(bind=engine)


class Session:
    table = None

    def __init__(self):
        self.session = session_bd(PATH)

    def get_all(self) -> iter:
        """Получить все записи таблицы"""
        with self.session() as sess:
            users = sess.query(self.table)
        return iter(users.all())
