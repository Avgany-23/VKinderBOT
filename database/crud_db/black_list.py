# Импортируем необходимые модули
import sqlalchemy
from sqlalchemy.orm import sessionmaker
# Импортируем настройки базы данных из файла settings.py
from settings import DATABASES
# Импортируем модель BlackList из файла database/models.py
from database.models import BlackList


class Connectbase:
    """Конструктор класса принимает аргументы данные пользователя VK"""
    def __init__(self, a, b, c, d):
        pass

        self.data_bd = DATABASES['postgresql']
        """Формируем строку подключения к базе данных"""
        self.path = (f"{self.data_bd['NAME']}://{self.data_bd['USER']}:{self.data_bd['PASSWORD']}@"
                     f"{self.data_bd['HOST']}:{self.data_bd['PORT']}/{self.data_bd['BD_NAME']}")

    def blacklist(self):
        pass