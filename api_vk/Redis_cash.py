import redis
import json
from main import users_data #ВАЖНО! для users_data в main нужен токен=ключ доступа пользователя


"""users_data-это список со словарями, нужен словарь """
users_dict = {user['id']: user for user in users_data}

# Подключаемся к Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

#найти пользователя в кеше по id
def find_in_cash_with_id(id: int):
    try:
        user_info = r.get(f'user:{id}')
        user_info = json.loads(user_info)  # Преобразуем обратно в словарь
    except TypeError:
        return 'Пользователь не найден в кэше.'
    return user_info if user_info else 'Пользователь не найден в кэше.'

#Для сброса кеша команда flushdb() - приведет к удалению всех данных в текущей базе данных Redis
def clear_cache() -> str:
    r.flushdb()  # Это удалит все ключи в текущей базе данных
    return 'Кэш очищен'

# Функция для обновления всего кеша
def update_cache() -> str:
    for user_id, info in users_dict.items():
        # Сохраняем каждого пользователя в Redis
        r.set(f'user:{user_id}', json.dumps(info))
    return 'Кэш обновлен'

#Выведем все, что у нас есть в кеше
def print_all_users() -> str | list:
    user_keys = r.keys('user:*')  # Получаем все ключи, начинающиеся с 'user:'
    all_users = []
    for key in user_keys:
        user_info = r.get(key)  # Получаем данные по ключу
        if user_info: # Проверяем, что user_info не пустое или None
            user_info = json.loads(user_info)  # Преобразуем обратно в словарь
            all_users.append(user_info)
    return all_users if all_users else 'Пользователь не найден в кэше.'

#Удаление пользователя по id
def delete_user(id: int) -> str:
    r.delete(f'user:{id}')
    return 'Пользователь удален из Redis'



