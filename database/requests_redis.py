from redis import Redis
from settings import DATABASES
import redis
import json


def redis_connect(path: dict = DATABASES['redis'], charset_: bool = True) -> tuple[str, ConnectionError] | Redis:
    """Подключение к редису"""
    redis_data = path
    encoding = {'charset': redis_data['charset']} if charset_ else {'encoding': redis_data['charset']}
    try:
        connect = redis.StrictRedis(host=redis_data['host'],
                                    port=redis_data['port'],
                                    db=redis_data['db'],
                                    decode_responses=redis_data['decode_responses'],
                                    **encoding)
    except redis.exceptions.ConnectionError as e:
        return 'Ошибка при подключении к Redis', e
    return connect


def redis_set_person(id_user: int, message: dict, connect: redis.StrictRedis = redis_connect()) -> None:
    """Для записи в redis"""
    redis_r = connect
    key = f"search_{id_user}"
    redis_r.lpush(key, json.dumps(message))
    if redis_r.llen(key) > 3:
        redis_r.rpop(key)
    redis_r.close()


def redis_set_current_person(id_user: int, id_search_user: int, connect: redis.StrictRedis = redis_connect()) -> None:
    """Установить в памяти текущий id анкеты пользователя"""
    redis_r = connect
    redis_r.set(f'current_person_{id_user}', id_search_user)
    redis_r.close()


def redis_get_current_person(id_user: int, connect: redis.StrictRedis = redis_connect()) -> str:
    """Получить id текущей анкеты пользователя"""
    redis_r = connect
    return redis_r.get(f'current_person_{id_user}')


def redis_get_person_info(id_user: int, connect: redis.StrictRedis = redis_connect()) -> dict:
    """Получить информацию о последнем пользователе по id"""
    redis_r = connect
    list_keys = [json.loads(i) for i in redis_r.lrange(f"search_{id_user}", 0, -1)]
    return list_keys[-1]


def redis_get_person_current_info(id_user: int, connect: redis.StrictRedis = redis_connect()) -> dict:
    """Получить полную информацию о текущем пользователе"""
    redis_r = connect
    current_person_indx = redis_r.get(f'current_person_{id_user}')
    for people in [json.loads(i) for i in redis_r.lrange(f'search_{id_user}', 0, -1)]:
        if people['id_user'] == int(current_person_indx):
            return people


def redis_person_is_current(id_user: int, connect: redis.StrictRedis = redis_connect()) -> bool:
    """Проверить, находимся ли на текущей анкете"""
    redis_r = connect
    list_keys = [json.loads(i)['id_user'] for i in redis_r.lrange(f"search_{id_user}", 0, -1)]
    try:
        return int(list_keys[0]) == int(redis_get_current_person(id_user, connect=redis_r))
    except KeyError:
        return True


def redis_person_is_last(id_user: int, connect: redis.StrictRedis = redis_connect()) -> bool:
    """Проверить, находимся ли на последней анкете"""
    redis_r = connect
    list_keys = [json.loads(i)['id_user'] for i in redis_r.lrange(f"search_{id_user}", 0, -1)]
    return int(list_keys[-1]) == int(redis_get_current_person(id_user, connect=redis_r))


def redis_get_prev_person(id_user: int, connect: redis.StrictRedis = redis_connect()) -> dict | str:
    """Получить информацию о предыдущей анкете"""
    redis_r = connect
    try:
        current_persons = [json.loads(i) for i in redis_r.lrange(f'search_{id_user}', 0, -1)]
        current_persons_list = [i['id_user'] for i in current_persons]
    except IndexError:
        return 'empty list'
    current_person = redis_r.get(f'current_person_{id_user}')
    prev_person_index = current_persons_list.index(int(current_person)) + 1
    if len(current_persons_list) <= prev_person_index:
        return 'end list'
    prev_person_id = current_persons_list[prev_person_index]
    for person in current_persons:
        if person['id_user'] == prev_person_id:
            return person


def redis_get_next_person(id_user: int, connect: redis.StrictRedis = redis_connect()) -> dict | str:
    redis_r = connect
    try:
        current_persons = [json.loads(i) for i in redis_r.lrange(f'search_{id_user}', 0, -1)]
        current_persons_list = [i['id_user'] for i in current_persons]
    except IndexError:
        return 'empty list'
    current_person = redis_r.get(f'current_person_{id_user}')
    prev_person_index = current_persons_list.index(int(current_person)) - 1
    if len(current_persons_list) <= prev_person_index:
        return 'end list'
    prev_person_id = current_persons_list[prev_person_index]
    for person in current_persons:
        if person['id_user'] == prev_person_id:
            return person


def redis_clear_user_id(id_user: int, connect: redis.StrictRedis = redis_connect()) -> None:
    redis_r = connect
    redis_r.delete(f'current_person_{id_user}')
    redis_r.delete(f'search_{id_user}')


def redis_save_history(id_user: int,
                       message: dict,
                       size: int = 15,
                       connect: redis.StrictRedis = redis_connect()) -> None:
    """Запись анкеты в Redis для дальнейшего её просмотра"""
    redis_r = connect
    key = f'history_{id_user}'
    redis_r.lpush(key, json.dumps(message))
    if redis_r.llen(key) > size:
        redis_r.rpop(key)


def redis_browsing_history(id_user: int, connect: redis.StrictRedis = redis_connect()) -> str:
    """Из таблицы с историей просмотров достает последние count записей"""
    redis_r = connect
    key = f'history_{id_user}'
    history = [json.loads(element) for element in redis_r.lrange(key, 0, -1)]
    people = '\n'.join(f"{i}){person['message']}"
                       f"Ссылка: {person['url_profile']}\n" for i, person in enumerate(history, 1))
    return f"Ваша история просмотров последних {len(history)} записей:\n{people}"


def redis_info_user(id_user: int,
                    info: dict,
                    action: str = 'save',
                    connect: redis.StrictRedis = redis_connect()) -> None | dict:
    """Сохраняет и изымает информацию о текущей анкете"""

    key = f'info_user_vk_{id_user}'
    if action == 'save':
        connect.set(key, json.dumps(info))
        connect.close()
        return None
    else:
        result = json.loads(connect.get(key))
        connect.close()
        return result
