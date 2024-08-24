from database.models import BlackList
from database import Session


class BlackListBD(Session):
    table = BlackList

    def BlackListBD(self):
        pass