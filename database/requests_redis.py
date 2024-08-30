from redis import Redis
from settings import DATABASES
import redis
import json


def redis_connect() -> tuple[str, ConnectionError] | Redis:
    """Подключение к редису"""
    redis_data = DATABASES['redis']
    try:
        connect = redis.StrictRedis(host=redis_data['host'],
                                    port=redis_data['port'],
                                    db=redis_data['db'],
                                    decode_responses=redis_data['decode_responses'],
                                    charset=redis_data['charset'],)
    except redis.exceptions.ConnectionError as e:
        return 'Ошибка при подключении к Redis', e
    return connect


def redis_set_person(id_user: int, message: dict) -> None:
    """Для записи в redis"""
    redis_r = redis_connect()
    key = f"search_{id_user}"
    redis_r.lpush(key, json.dumps(message))
    if redis_r.llen(key) > 3:
        redis_r.rpop(key)
    redis_r.close()


def redis_set_current_person(id_user: int, id_search_user: int) -> None:
    """Установить в памяти текущий id анкеты пользователя"""
    redis_r = redis_connect()
    redis_r.set(f'current_person_{id_user}', id_search_user)
    redis_r.close()


def redis_get_current_person(id_user: int) -> str:
    """Получить id текущей анкеты пользователя"""
    redis_r = redis_connect()
    return redis_r.get(f'current_person_{id_user}')


def redis_get_person_info(id_user: int) -> dict:
    """Получить информацию о последнем пользователе по id"""
    redis_r = redis_connect()
    list_keys = [json.loads(i) for i in redis_r.lrange(f"search_{id_user}", 0, -1)]
    return list_keys[-1]


def redis_person_is_current(id_user: int) -> bool:
    """Проверить, находимся ли на последней анкете"""
    redis_r = redis_connect()
    list_keys = [json.loads(i)['id_user'] for i in redis_r.lrange(f"search_{id_user}", 0, -1)]
    try:
        return int(list_keys[0]) == int(redis_get_current_person(id_user))
    except KeyError:
        return True


def redis_person_is_last(id_user: int) -> bool:
    """Проверить, находимся ли на последней анкете"""
    redis_r = redis_connect()
    list_keys = [json.loads(i)['id_user'] for i in redis_r.lrange(f"search_{id_user}", 0, -1)]
    return int(list_keys[-1]) == int(redis_get_current_person(id_user))


def redis_get_prev_person(id_user: int) -> dict | str:
    redis_r = redis_connect()
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


def redis_get_next_person(id_user: int) -> dict | str:
    redis_r = redis_connect()
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


def redis_clear_user_id(id_user: int) -> None:
    redis_r = redis_connect()
    redis_r.delete(f'current_person_{id_user}')
    redis_r.delete(f'search_{id_user}')


def redis_save_history(id_user: int, message: dict, size: int = 15) -> None:
    """Запись анкеты в Redis для дальнейшего её просмотра"""
    redis_r = redis_connect()
    key = f'history_{id_user}'
    redis_r.lpush(key, json.dumps(message))
    if redis_r.llen(key) > size:
        redis_r.rpop(key)


def redis_browsing_history(id_user: int) -> str:
    """Из таблицы с историей просмотров достает последние count записей"""
    redis_r = redis_connect()
    key = f'history_{id_user}'
    history = [json.loads(element) for element in redis_r.lrange(key, 0, -1)]
    people = '\n'.join(f"{i}){person['message']}"
                       f"Ссылка: {person['url_profile']}\n" for i, person in enumerate(history, 1))
    return f"Ваша история просмотров последних {len(history)} записей:\n{people}"
