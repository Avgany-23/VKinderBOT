from database.models import BlackList
from database import Session


class BlackListBD(Session):
    table = BlackList
    """Конструктор класса принимает аргументы данные пользователя VK"""

    def likedlist(self):
        pass