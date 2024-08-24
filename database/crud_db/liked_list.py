from database.models import LikedList
from database import Session


class LikedListBD(Session):
    table = LikedList
    """Конструктор класса принимает аргументы данные пользователя VK"""

    def likedlist(self):
        pass