# Импортируем необходимые модули
import sqlalchemy
from sqlalchemy.orm import sessionmaker
# Импортируем настройки базы данных из файла settings.py
from settings import DATABASES
# Импортируем модель Users из файла database/models.py
from database.models import Users


"""Определяем класс Connectbase для подключения к базе данных"""
class Connectbase:
    """Конструктор класса принимает идентификатор пользователя VK"""
    def __init__(self, id_vk):
        """Сохраняем настройки базы данных"""
        self.data_bd = DATABASES['postgresql']
        """Формируем строку подключения к базе данных"""
        self.path = (f"{self.data_bd['NAME']}://{self.data_bd['USER']}:{self.data_bd['PASSWORD']}@"
                    f"{self.data_bd['HOST']}:{self.data_bd['PORT']}/{self.data_bd['BD_NAME']}")
        """Сохраняем идентификатор пользователя"""
        self.id_vk = id_vk


    def createuser(self):
        """Функция для создания пользователя в базе данных"""
        """Создаем соединение с базой данных"""
        engine = sqlalchemy.create_engine(self.path)
        """Создаем сессию для работы с базой данных"""
        Session = sessionmaker(bind=engine)
        """Используем контекстный менеджер для работы с сессией"""
        with Session() as session:
            """Добавляем нового пользователя в базу данных"""
            session.add(Users(id_vk=self.id_vk))
            """Фиксируем изменения в базе данных"""
            session.commit()
            """Выводим сообщение об успешном создании пользователя"""
            print(f"Пользоваль ID: {self.id_vk} - создан")


# Задаем идентификатор пользователя VK для регистрации
id_vk = 1234537


"""Регистрация пользователя"""
Connectbase(id_vk).createuser()
