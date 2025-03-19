# Telegram-бот для поздравлений менторов Devman

## Описание

Этот бот помогает автоматически поздравлять менторов с праздниками, предоставляя удобный интерфейс для выбора ментора и отправки персонализированной открытки. Сделайте поздравления более удобными и эффективными!

## Структура проекта
### Основные файлы и директории:
- `main.py:` Главный файл для запуска Telegram-бота. Настраивает обработчики команд и сообщений.
- `libs/api_client/api_requests.py:`
    - `get_postcards:` извлекает и валидируют данные об открытках через Pydantic-модель, проверяя их формат на соответствие ожидаемым моделям.  
    - `get_mentors:` извлекает и валидируют данные о менторах через Pydantic-модель, проверяя их формат на соответствие ожидаемым моделям. 
    - `handle_error_response:` декоратор обработок ошибок запросов API.
- `handlers/handlers.py:` Обработчики событий Telegram-бота, включая команды и сообщения.
- `libs/utils.py:` 
    - `format_long_name:` Форматирования длинных имен менторов.
    - `start_role:` Определяет роль пользователя (ментор или ученик) на основе его Telegram ID.
    - `insert_name:` Вставляет имя в открыту поздравления.
    - `message_splitter:` Обрезает сообщения, которые более 4096 длинной.
- `libs/arg_parser:` Парсер аргументов командной строки и тестовых сценариев. 
- `tests/api_test.py:` Скрипт для запуска локального тестового FastAPI сервера.

## Функциональность бота
1. `Команда /start:`

    - Приветствует пользователя и определяет его роль (ментор или ученик).

    - Показывает клавиатуру с кнопками:
        - "Показать менторов"
        - "Показать открытки"

2. `Кнопки:`

    - "Показать менторов": Отображает список менторов с их именами и ссылками на Telegram.
    - "Показать открытки": Показывает список доступных открыток.

3. `Выбор ментора и отправка открытки:`

    - Пользователь выбирает ментора из списка.
    - Затем выбирает открытку, которая будет отправлена выбранному ментору.

4. `Обработка ошибок:`

    - Обрабатываются ошибки Telegram API (например, пользователь заблокировал бота).
    - Предоставляются сообщения об ошибках при некорректных действиях.

5. `Восстановление состояние:`

    - Если бот был приостановлен, то при запуске команды `/start` он продолжит с места остановки.

## Установка
1. Клонируйте репозиторий:

    ```python
    git clone <URL репозитория>
    cd <имя директории>
    ```
2. Установите зависимости:
    ```python
    pip install -r requeriments.txt
    ```
3. Создайте файл .env в корне проекта и добавьте ваш Telegram токен:
    ```text
    TG_TOKEN=ваш_токен_бота
    ```

## Локальный сервер API для тестирования

Для тестирования бота, вы можете развернуть локальный сервер API.

### Шаги по развертыванию локального сервера и его запуск:
1. Установите FastAPI и Uvicorn:

    ```bash
    pip install fastapi uvicorn
    ```

### Тестовый сервер

1. Перейдите в директорию с файлом `tests/api_test.py`.
2. Запустите сервер с помощью Uvicorn:
        ```
        uvicorn api_mentors:app --host 127.0.0.1 --port 8002 --reload
        ```
*   `api_test:app` - указывает на файл `api_test.py` и экземпляр FastAPI приложения `app`.
*   `--host 127.0.0.1` - задает хост для сервера (localhost).
*   `--port 8002` - задает порт для сервера.
*   `--reload` - включает автоматическую перезагрузку сервера при изменении кода.

3. После запуска сервер будет доступен по адресу: `http://127.0.0.1:8002`


## Доступные эндпоинты

### Тестовый сервер (http://127.0.0.1:8002)
*   `/empty_list:` Возвращает пустой список менторов и открыток.
*   `/large_list:` Возвращает список из 30 менторов и 130 открыток.
*   `/standard_list:` Возвращает список из 3 менторов и 5 открыток.
*   `/long_name:` Возвращает ментора с очень длинным именем и дилнную открытку из 500 слов.
*   `/invalid_json:` Возвращает JSON с ошибкой в синтаксисе.
*   `/not_match_scheme:` Возвращает данные, не соответствующие схеме (например, неправильные типы данных).
*   `/excess_data:` Возвращает дополнительные данные, не предусмотренные схемой.
*   `/mentor_status:` Возвращает информацию об одном менторе (нужно указать ваши данные в json) и открытки с #name для вставки имени.
*   `/default:` По умолчанию не тестовые url's.

#### Пример ответа для `/mentor_status`:
* `http://127.0.0.1:8002/mentor_info`
    ```python
        {"mentors": 
        [
            {"id": 1, "name": {"first": "Евгений", "second": "Devman"}, "tg_username": "@e", "tg_chat_id": 2321, "birthday": "1991-02-23"}, 
            {"id": 2, "name": {"first": "Ильмир", "second": "Devman"}, "tg_username": "@il", "tg_chat_id": 32, "birthday": None}, 
            {"id": 3, "name": {"first": "Роман", "second": "Грч"}, "tg_username": "@R", "tg_chat_id": 123123, "birthday": "1991-02-23"}
        ]
        }
    ```

* `http://127.0.0.1:8002/name_template`
    ```python
        {"postcards": 
        [
            {"id": 1, "holiday_name": "01.01", "name_ru": "Новый год", "body": "🎉✨#name, С Новым годом! Пусть этот год принесёт тебе радость, процветание и успех!✨🎉"}, 
            {"id": 2, "holiday_name": "01.07", "name_ru": "Рождество Христово (Православие)", "body": "🌟 #name,С Рождеством Христовым! Христос рождается!🌟"}, 
            {"id": 40, "holiday_name": "birthday", "name_ru": "День рождения", "body": "💐🌸 #name, С Днём рождения! Пусть твоя жизнь будет похожа на прекрасный сад, где каждое мгновение расцветает новыми красками! Желаю безграничного счастья, мира и благополучия! 🌸💐"}
        ]
        }
    ```
## Запуск
Запуск Telegram-бота через командную строку и по следующим сценариям:
    
1. Основной (рекомендуется), запуск с не тестовыми url's:
        ```
        python main.py
        ```
2. Возвращает пустой список менторов и открыток:
        ```
        python main.py empty_list
        ```
3. Возвращает список из 30 менторов и 130 открыток:
        ```
        python main.py large_list
        ```
4. Возвращает список из 3 менторов и 5 открыток:
        ```
        python main.py standard_list
        ```
5. Возвращает ментора с очень длинным именем и дилнную открытку из 500 слов:
        ```
        python main.py long_name
        ```
6. Возвращает JSON с ошибкой в синтаксисе:
        ```
        python main.py invalid_json
        ```
7. Возвращает данные, не соответствующие схеме (например, неправильные типы данных):
        ```
        python main.py not_match_scheme
        ```
        
8. Возвращает информацию об одном менторе (нужно указать ваши данные в json) и открытки с #name для вставки имени:
        ```
        python main.py mentor_status
        ```
9. Запуск с параметром --token, запуск происходит с вашим токеном тг бота:
        ```
        python main.py mentor_status --token 
        ```

## Обработка ошибок

Приложение обрабатывает различные типы ошибок для обеспечения стабильности и информативности. Ниже приведены основные типы ошибок и их описание:

1.  **Сетевые ошибки (`NetworkError`)**

    Эти ошибки возникают при проблемах с сетевым соединением, например, если сервер недоступен или нет соединения с Интернетом.

2.  **Ошибки формата ответа (`ResponseFormatError`)**

    Эти ошибки возникают, когда ответ от сервера имеет неожиданный формат, что может привести к проблемам с парсингом данных.

3.  **Ошибки сервера (`ServerError`)**

    Эти ошибки включают в себя различные проблемы на стороне сервера, такие как невалидный JSON, неправильные HTTP-запросы или ошибки аутентификации.

4.  **Общие ошибки**

    Любые другие необработанные исключения также обрабатываются и регистрируются для дальнейшего анализа.

### Примеры ошибок:

- `JSONDecodeError`: Возникает при невалидном JSON в ответе от сервера.
- `httpx.RequestError`: Обработка ошибок запросов, включая соединения и таймауты.
- `httpx.HTTPStatusError`: Обработка HTTP-статусов, отличных от 2xx, таких как 404 или 500.


## Лицензия
MIT