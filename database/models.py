from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy import Column, Integer, BigInteger, Sequence, ForeignKey

basic = declarative_base()


class Users(basic):
    """Модель пользователей"""
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), autoincrement='auto')
    id_vk = Column(BigInteger, primary_key=True)

    infouser: Mapped['InfoUsers'] = relationship(back_populates='users', uselist=False)
    blacklist: Mapped['BlackList'] = relationship(back_populates='users', uselist=True)
    likedlist: Mapped['LikedList'] = relationship(back_populates='users', uselist=True)


class InfoUsers(basic):
    """Модель с информацией о пользователях"""
    __tablename__ = 'infousers'

    id = Column(BigInteger, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'), unique=True)

    users: Mapped['Users'] = relationship(back_populates='infouser', uselist=False)


class BlackList(basic):
    """Модель списка игнорируемых пользователей"""
    __tablename__ = 'blacklist'

    id = Column(BigInteger, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'))
    id_ignore_user = Column(BigInteger, nullable=False, unique=True)

    users: Mapped['Users'] = relationship(back_populates='blacklist', uselist=False)


class LikedList(basic):
    """Модель отмеченных пользователей"""
    __tablename__ = 'likedlist'

    id = Column(BigInteger, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'))
    id_like_user = Column(BigInteger, nullable=False, unique=True)

    users: Mapped['Users'] = relationship(back_populates='likedlist', uselist=False)