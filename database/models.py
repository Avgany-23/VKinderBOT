from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy import Column, Integer, BigInteger, Sequence, ForeignKey, CHAR, UniqueConstraint, Text, Boolean, Date, \
    Index

basic = declarative_base()


class Users(basic):
    """Модель пользователей"""
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), autoincrement='auto')
    id_vk = Column(BigInteger, primary_key=True)

    id_vk_index = Index('idx_users_id_vk', id_vk)

    infouser: Mapped['InfoUsers'] = relationship(back_populates='users', uselist=False)
    blacklist: Mapped['BlackList'] = relationship(back_populates='users', uselist=True)
    likedlist: Mapped['LikedList'] = relationship(back_populates='users', uselist=True)
    userfilter: Mapped['FiltersUsers'] = relationship(back_populates='users', uselist=False)
    searchpeople: Mapped['SearchPeople'] = relationship(back_populates='users', uselist=True)

    def __str__(self):
        return f"id_vk: {self.id_vk}"


class InfoPeople:
    id = Column(Integer, primary_key=True)
    # id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'), unique=True)
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


class InfoUsers(basic, InfoPeople):
    """Модель с информацией о пользователях"""
    __tablename__ = 'infousers'
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'), unique=True)

    users: Mapped['Users'] = relationship(back_populates='infouser', uselist=False)

    id_user_index = Index('idx_infousers_id_user', id_user)


class SearchPeople(basic):
    """Для хранения людей, которые будут выдаваться пользователю при показе анкет"""
    __tablename__ = 'searchpeople'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger)
    id_user_main = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'))

    users: Mapped['Users'] = relationship(back_populates='searchpeople', uselist=False)

    id_user_index = Index('idx_searchpeople_id_user', id_user)
    id_user_main_index = Index('idx_searchpeople_id_user_main', id_user_main)

    __table_args__ = (
        UniqueConstraint('id_user', 'id_user_main', name='unique_user_search_users'),
    )


class BlackList(basic):
    """Модель списка игнорируемых пользователей"""
    __tablename__ = 'blacklist'

    id = Column(BigInteger, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.id_vk', ondelete='CASCADE'))
    id_ignore_user = Column(BigInteger, nullable=False)
    name_user = Column(Text, nullable=True)

    id_user_index = Index('idx_blacklist_id_user', id_user)
    id_ignore_user_index = Index('idx_blacklist_id_ignore_user', id_ignore_user)

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
    name_user = Column(Text, nullable=True)

    id_user_index = Index('idx_likedlist_id_user', id_user)
    id_like_user_index = Index('idx_likedlist_id_like_user', id_like_user)

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

    id_user_index = Index('idx_filtersusers_id_user', id_user)

    users: Mapped['Users'] = relationship(back_populates='userfilter', uselist=False)