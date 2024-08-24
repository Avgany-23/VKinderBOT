from database.models import LikedList
from database import Session


class LikedListBD(Session):
    table = LikedList

    def likedlist(self):
        pass