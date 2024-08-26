from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy import Column, Integer, BigInteger, Sequence, ForeignKey, CHAR, UniqueConstraint, Text, Boolean, Date

basic = declarative_base()


class Users(basic):
    """Модель пользователей"""
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), autoincrement='auto')
    id_vk = Column(BigInteger, primary_key=True)

    infouser: Mapped['InfoUsers'] = relationship(back_populates='users', uselist=False)
    blacklist: Mapped['BlackList'] = relationship(back_populates='users', uselist=True)
    likedlist: Mapped['LikedList'] = relationship(back_populates='users', uselist=True)
    userfilter: Mapped['FiltersUsers'] = relationship(back_populates='users', uselist=False)

class InfoUsers(basic):
    """Модель с информацией о пользователях"""
    __tablename__ = 'infousers'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'), unique=True)
    first_name = Column(CHAR(length=255))
    last_name = Column(CHAR(length=255))
    screen_name = Column(CHAR(length=255))
    sex = Column(Integer)
    can_access_closed = Column(Boolean)
    is_closed = Column(Boolean)
    bdate = Column(Date)
    city_id = Column(Integer)
    city_title = Column(CHAR(length=255))
    interests = Column(Text)
    about = Column(Text)
    activities = Column(Text)
    music = Column(Text)
    relation = Column(Integer)

    users: Mapped['Users'] = relationship(back_populates='infouser', uselist=False)


class BlackList(basic):
    """Модель списка игнорируемых пользователей"""
    __tablename__ = 'blacklist'

    id = Column(BigInteger, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'))
    id_ignore_user = Column(BigInteger, nullable=False)

    users: Mapped['Users'] = relationship(back_populates='blacklist', uselist=False)

    __table_args__ = (
        UniqueConstraint('id_user', 'id_ignore_user', name='unique_user_black_user'),
    )


class LikedList(basic):
    """Модель отмеченных пользователей"""
    __tablename__ = 'likedlist'

    id = Column(BigInteger, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'))
    id_like_user = Column(BigInteger, nullable=False)

    users: Mapped['Users'] = relationship(back_populates='likedlist', uselist=False)

    __table_args__ = (
        UniqueConstraint('id_user', 'id_like_user', name='unique_user_like_user'),
    )


class FiltersUsers(basic):
    """Модель с информацией о пользователях"""
    __tablename__ = 'filtersusers'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'), unique=True)
    sex = Column(Integer, nullable=False)
    age_from = Column(Integer, nullable=False, default=14)
    age_to = Column(Integer, nullable=False, default=100)
    city_id = Column(Integer, default=1)
    city_title = Column(CHAR(length=255), default='Москва')
    relation = Column(Integer, default=0)

    users: Mapped['Users'] = relationship(back_populates='userfilter', uselist=False)