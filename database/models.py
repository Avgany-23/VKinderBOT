from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Sequence

basic = declarative_base()


class Users(basic):
    """Модель пользователей"""
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), autoincrement='auto')
    id_vk = Column(BigInteger, primary_key=True)


class InfoUsers(basic):
    """Модель с информацией о пользователях"""


class BlackList(basic):
    """Модель списка игнорируемых пользователей"""


class LikedList(basic):
    """Модель отмеченных пользователей"""
