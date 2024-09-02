# **VK BOT для поиска людей** + bot tg для отправки уведомлений

## Стек технологий: Python 3.11 (SQLalchemy ORM, VkApi, telebot, threading, unittest), PostgreSQL, Redis

> ### _[Настройка по установке проекта](./INSTALLATION_MANUAL.md)_
> ### _[Техническая документация](./CodeDocumentation.md)_

----

### _Возможности бота_

--при вводе слова "меню" бот открывает нижнюю панель клавиш

<p align="center">
  <img src="https://github.com/user-attachments/assets/261d9551-1036-4b54-a83b-ce6a60368415">
</p>

- "Ваши отметки" - бот покажет количество человек, который добавили вас к себе в личный список, используя этот же бот

- "История просмотром" - бот покажет последние 15 анкет, которые вы просмотрели

- "Like list" и "Block list" - бот покажет пользователей, которых вы сохранили в список избранных людей или в черный список при просмотре анкет

- "фильтры поиска людей" - бот выведет список текущих и список доступных фильтров, при которых будет происходить поиск людей:

<p align="center">
  <img src="https://github.com/user-attachments/assets/df1da3b0-e397-4db7-99fa-60df6c9b9909">
</p>

- "найти половинку" - бот по указанным фильтрам начнет искать пользователей вк. Если фильтры не указаны, то он автоматически подберёт нужные фильтры для пользователя

<p align="center">
  <img src="https://github.com/user-attachments/assets/33fc8976-12cd-4edc-82dd-acf1d53b3c48">
</p>


_При поиске анкеты будет выведена краткая информация о ней и до трех фотографий, можно перемещаться на следующего и предыдущего пользователя, а также добавить его в список избранного (чтобы потом вернуться к нему), заблокировать его (чтобы больше эта анкета не показывалась) и перейти по ссылке на страницу пользователя._

**Все данные (Фильтры, списки) сохраняются в базу данных и кеш по id_vk пользователя.**

> [!IMPORTANT]
> **Все данные (фильтры, списки) сохраняются в базу данных и кеш по id_vk пользователя.**
> Администраторам бота будет доступен отдельный TG bot для посмотра логов работы программы
