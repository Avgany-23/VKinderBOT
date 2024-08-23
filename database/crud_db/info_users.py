# Импортируем необходимые модули
import sqlalchemy
from sqlalchemy.orm import sessionmaker
# Импортируем настройки базы данных из файла settings.py
from settings import DATABASES
# Импортируем модель InfoUsers из файла database/models.py
from database.models import InfoUsers


"""Определяем класс Connectbase для подключения к базе данных"""
class Connectbase:
    """Конструктор класса принимает аргументы данные пользователя VK"""
    def __init__(self, *args):
        """Сохраняем настройки базы данных"""
        self.data_bd = DATABASES['postgresql']
        """Формируем строку подключения к базе данных"""
        self.path = (f"{self.data_bd['NAME']}://{self.data_bd['USER']}:{self.data_bd['PASSWORD']}@"
                     f"{self.data_bd['HOST']}:{self.data_bd['PORT']}/{self.data_bd['BD_NAME']}")
        """Распаковываем информацию о пользователе"""
        self.id_user = args[0]
        self.name = args[1]
        self.age = args[2]
        self.gender = args[3]
        self.marital_status = args[4]
        self.city = args[5]
        self.interests = args[6]


    def infousers(self):
        """Функция для записи информации о пользователе"""
        """Создаем соединение с базой данных"""
        engine = sqlalchemy.create_engine(self.path)
        """Создаем сессию для работы с базой данных"""
        Session = sessionmaker(bind=engine)
        """Используем контекстный менеджер для работы с сессией"""
        with Session() as session:
            """Добавляем информацию о пользователе"""
            session.add(InfoUsers(id_user=self.id_user,
                                  name=self.name,
                                  age=self.age,
                                  gender=self.gender,
                                  marital_status=self.marital_status,
                                  city=self.city,
                                  interests=self.interests
                                  ))
            """Фиксируем изменения в базе данных"""
            session.commit()
            """Выводим сообщение об успешном создании пользователя"""
            print(f"Пользоваль ID: {self.id_user} - создан")

id_user = "1234537"
name = "Ловелас"
age = 21
gender = "мужской"
marital_status = "активный поиск"
city = "Москва"
interests = "Музыка"


args = [id_user, name, age, gender, marital_status, city, interests]
print(args[1])
Connectbase(*args).infousers()