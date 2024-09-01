# Техническое описание проекта

----

## 1. Общее:

- при запуске главного файла main.py создаётся База данных в PostgreSQL и все необходимые таблицы в ней. Если База данных или таблицы уже созданы, то повторное создание не произойдёт;
- при нажатии на кнопку "Найти половинку" или "Фильтры для поиска" - происходит первичная инициализация пользователя, данные о нём сохраняются 1 раз в в PostgreSQL;
- информация о фильтрах, список избранного/чс, фильтры пользователя, подходящие люди для показа сохраняются в PostgreSQL;
- весь кеш (чтобы переходить на предыдущую анкету, показ истории просмотров и т.д.) сохраняется в Redis;
- tg bot также сохраняет информацию о пользователях в кеш (только tg_id пользователей, которые им пользуются).

2. Модуль main.py в директории проекта:

Модуль выполняет три гланвых действия во время запусках:
1) создание Базы Данных и таблиц в PostgreSQL, если они ещё не созданы
2) запускает телеграм бота, если он включен в ```settings.py```
3) запускает самого бота ВК

В модуле также расставлены логи об основных действиях и ошибках программы, которые будут отправлять в телеграм бот к пользователю.

Бот ВК и ТГ работают параллельно за счет двух процессов threading.Thread() библиотеки threading.

3. Модуль settings.py в главной директории проекта:

В модуле прописаны настройки, которые необходимо верно указать при подключении к PostgreSQL, Redis и TG боту. Также можно выбрать размер кеша в переменной ```HISTORY_SIZE```, которая отвечает за то, сколько анкет в памяти будут сохраняться для истории просмотров.

При необходимости можно указать версию VK API в переменной ```HISTORY_SIZE```

4. Модуль test_settings.py в главной директории проекта:

Модуль предназначен для настройки PostgreSQL и Redis для тестов. Важно указать базу данных отличную от той, что используется основной программой, чтобы не потерять данные.

5. Директория tests_project:

В директории находятся основные unittest для тестирования программы. Для корректной работы всех тестов в файле ```.env``` необходимо указать все данные для тестов. Для тестов желательно иметь другие токены для VK API и VK BOT. 

6. Модуль vk_bot_main.py в главной директории проекта:

В данном модуле представлена одна функция vk_bot, которая ничего не принимает и не возвращает. Она запускает ВК бота и определяет основную его работу, используя функции в директориях api_vk, database и vk_bot.

При каждом отправленном сообщении или нажатой кнопки пользователем в чате с ВК ботом отправляется запрос в данную функцию, после чего он обрабатывается и БОТ возвращает ответ пользователю.

7. Директория logs:

Директория предназначена для работы ТГ бота, работающего в модуле tg_bot.py. Бот отправляет логи (написанные в файле logs.py) по следующей логике:
- если бот включен, то он будет ждать, пока хотя бы один пользователь в нем зарегистрируется, введя к нему в чат с логином и паролем от бота, указанные в settings.py;
- после запускает параллельный процесс за счет библиотеки threading и цикла while, активируя отправку уведомлений;
- уведомления о стандартных логах будут отправляются согласно времени, которое стоит у вас в настройках к боту в settings.ph (ключ send_time). Если будут получены логи о критических ошибках, которые могут остановить или остановили работу бота ВК, то информация о таких ошибках будет отправлено сразу же в чат к пользователю, вне зависимости от того, какое время стоит в send_time. Бот будет отправлять файлы с логами всем пользователям, которые в нём зарегистрируются. После отправки, файлы с логами (logs_base.log, logs_error.log и starts_programm.log в директории logs) будут автоматически очищены, чтобы не засорять память.

8. Директория api_vk:

Директория содержит модуль main.py с классом SearchVK, который принимает токен от АПИ ВК. Данный класс предоставляет следующие методы:

- get_user_vk(self, user_id: int) - возвращает информацию о пользователе в ВК по его user_id. Функция вернёт словарь с информацией, если она найдется, или строчку, если с токен от АПИ ВК по каким-либо причинам станет недоступен;
- get_users_vk(count: int = 1000, **kwargs) - метод находит count пользователей в вк (по умолчанию 1000) по указанным фильтрам в kwargs. В работе программы используются следующие фильтры:
  
1)sex: int (1 or 2)

2)city: int,

3)online: int (1 or 2),

4)age_from: int,

5)age_to: int,

6)has_photo: int (0 or 1),

7)is_closed: bool,

8)fields: str,

9)is_closed: boole.

- get_photo_user(self, user_id: int, place='profile', max_count: int = 5) - метод, по указанному user_id, достает от 0 до max_count (по умолчанию до 5) фотографий с профиля (place='profile') или со стены (place='wall') пользователя. Возвращает словарь с id фотографиями и дополнительной информацией о них. Вернёт -1, если при взятии фотографий не обнаружится какой-либо информации, например, ссылки на фотографию, количество лайков и т.д.

9. Директория database в главной директории проекта:

Директория содержит в себе функции и классы, необходимые для работы с PostgreSQL и Redis:

1) Директория crud_db - содержит в себе модули для работы моделями PostgreSQL. В них представлены CRUD запросы к базе данных на чтение, запись, удаление и обновление данных.
2) Модуль init.py - модуль содержит класс Session, от которого наследуются все классы в модулях crud_db. Класс содержит в себе информацию о подключении к PostgreSQL и 1 метод на чтение всех данных из используемой модели.
3) Модуль create_db - модуль предназначен для создание и удалении базы данных, создание моделей в БД и проверка их существования:
- create_object_db(path: str) - функция приниет path (str) - подключение к PostgreSQL и создает базу данных. Если БД с таким именем уже существует или неверно указан параметр path, то функция ничего не создат. Вернёт кортеж со статусом о создании. Если первый элемент кортежа равен 1, значит БД успешно создала, если -1, значит произошла ошибка в подключении к БД, -2, значит БД уже существует;
- check_bd(path_: str) - функция проверяет, есть ли в БД таблицы, которые указаны в модуле models.py этой же директории. Если таблиц нет, вернёт True, если есть хотя бы одна таблица, то вызовит исключение SystemExit;
- create_bd(info_path: str) - функция ничего не возвращает. Создает таблицы в указанной по info_path базе данных;
- delete_object_db(path: str) - функция по указанному path удаляет базу данных. Если удаление произошло без ошибок, то вернёт кортеж (1, None), если возникли ошибки sqlalchemy.exc.OperationalError или UnicodeDecodeError, то вернёт кортеж (-1, е), где е - информация об ошибке;
- create_bd_and_tables_if_not_exists() - функция предназначена только для работы программы. Функция ничего не принимает, по указанным настройкам в settings.py произведёт безопасное созадние БД и таблиц на основании предыдущих функций. Если БД с указанным в настройках именем уже будет существовать, то функция не станет пересоздавать БД, чтобы не стереть все имеющиеся в ней данные. Аналогично происходит и с созданием таблиц.

  