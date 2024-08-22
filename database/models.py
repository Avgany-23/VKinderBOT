from sqlalchemy.orm import declarative_base
from sqlalchemy import Column


basic = declarative_base()


class Users(basic): ...


class InfoUsers(basic): ...


class BlackList(basic): ...


class LikedList(basic): ...