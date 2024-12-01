# PulsePoll - Telegram Bot для Опросов

![Python](https://img.shields.io/badge/Python-3.12.3-blue.svg)
![aiogram](https://img.shields.io/badge/aiogram-3.13.0-blue)
![asyncpg_lite](https://img.shields.io/badge/asyncpg_lite-0.3.1.3-orange)

## Описание

**PulsePoll** - это Telegram-бот, разработанный с использованием библиотеки `aiogram`. Он предоставляет пользователям возможность создавать, удалять и управлять опросами, а также проходить доступные опросы. Результаты опросов могут быть экспортированы в формате Excel, что упрощает анализ данных.

## Функциональные возможности

- 📝 **Создание опросов**: Пользователи могут создавать новые опросы с вопросами и вариантами ответов.
- ❌ **Удаление опросов**: Удаление существующих опросов по запросу пользователя.
- 📋 **Управление опросами**: Просмотр списка доступных опросов и управление ими.
- ✅ **Участие в опросах**: Пользователи могут проходить доступные опросы и оставлять свои ответы.
- 📊 **Экспорт результатов**: Возможность отправки Excel-файла с результатами выбранного опроса. Также экспорт результатов в виде гистограмм.

## Технологии

- [Python](https://www.python.org/) - Язык программирования (версия 3.12.3).
- [aiogram](https://aiogram.readthedocs.io/en/latest/) - Асинхронная библиотека для работы с Telegram Bot API (версия 3.13.0).
- [asyncpg_lite](https://github.com/yourusername/asyncpg_lite) - Легковесная асинхронная библиотека для работы с 
  базой данных 
  (версия 0.3.1.3).

## Установка
1. 🛠️ Клонируйте репозиторий:

   ```bash
   git clone https://github.com/gultyy/pulsepoll.git
   cd pulsepoll
   ```
   
2. 📦 Установите зависимости:
    ```bash
    pip install -r requirements.txt
   ```
   
3. ⚙️ Настройте переменные окружения:
    Создайте файл .env в корневой директории проекта и добавьте следующие строки:
    ```bash
    ADMINS=123,345
    BOT_TOKEN=your_bot_token_here
    PG_LINK=postgresql://username:password@host:port/bd_name
   ```
    Замените username и password на ваши учетные данные для доступа к базе данных PostgreSQL.
    Добавьте telegram ID пользователей в ADMINS, которых хотите сделать админами вашего бота.

4. 🚀 Запустите бота:
    ```bash
    python run_bot.py
    ```

## Использование

   - 📱 Найдите вашего бота в Telegram, используя его имя пользователя (например, @PulsePoll).
   - 💬 Начните чат с ботом, отправив команду `/start`, чтобы начать взаимодействие.
   - 🛠️ Следуйте инструкциям бота для создания и управления опросами.

## Примеры команд

    /start - Начать взаимодействие с ботом.
    /take_poll - Пройти опрос.
    /stats - Статистика пройденных опросов.

## Структура проекта
    
    UrbanDiblomBot/
    ├── db_handler/
    │   ├── __init__.py
    │   └── db_funk.py
    ├── handlers/
    │   ├── __init__.py
    │   ├── admin_panel.py
    │   └── user_panel.py
    ├── keyboards/
    │   ├── __init__.py
    │   ├── kbs.py
    │   └── kbs_cfg.py
    ├── utils/
    │   ├── __init__.py
    │   └── my_utils.py
    ├── .env
    ├── .gitignore
    ├── create_bot.py
    ├── README.md
    ├── requirements.txt
    └── run_bot.py


