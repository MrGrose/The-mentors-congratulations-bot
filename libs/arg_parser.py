import argparse

from typing import Any

URL_CONFIG = {
    "empty_list": [
        "http://127.0.0.1:8002/mentors_no_items",
        "http://127.0.0.1:8002/postcards_no_items",
        ],
    "large_list": [
        "http://127.0.0.1:8002/thirty_mentors",
        "http://127.0.0.1:8002/postcards_130",
        ],
    "standard_list": [
        "http://127.0.0.1:8002/3_mentors", 
        "http://127.0.0.1:8002/postcards_5",
        ],
    "long_data": [
        "http://127.0.0.1:8002/long_name",
        "http://127.0.0.1:8002/long_postcard",
        ],
    "invalid_json": [
        "http://127.0.0.1:8002/mentors_invalid",
        "http://127.0.0.1:8002/postcards_invalid",
        ],
    "not_match_scheme": [
        "http://127.0.0.1:8002/mentors_not_shema",
        "http://127.0.0.1:8002/postcards_not_shema",
        ],
    "excess_data": [
        "http://127.0.0.1:8002/too_much_mentors",
        "http://127.0.0.1:8002/too_much_postcards",
        ],
    "mentor_status": [
        "http://127.0.0.1:8002/mentor_info",
        "http://127.0.0.1:8002/name_template",
        ],
    "default": [
        "https://my-json-server.typicode.com/devmanorg/congrats-mentor/mentors",
        "https://my-json-server.typicode.com/devmanorg/congrats-mentor/postcards",
        ]
}


def create_parser() -> tuple[str, str, Any]:
    """Создает парсер аргументов командной строки с поддержкой тестовых сценариев."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        Доступные тестовые сценарии (key):

        empty_list: Возвращает пустой список менторов и открыток
        large_list: Возвращает список из 30 менторов и 130 открыток
        standard_list: Возвращает список из 3 менторов и 5 открыток
        long_name: Возвращает ментора с именем из 15 слов и открытку из 500 слов
        invalid_json: Возвращает JSON с синтаксической ошибкой
        not_match_scheme: Возвращает данные с несоответствием схеме (неправильные типы)
        excess_data: Возвращает дополнительные данные вне схемы
        mentor_status: Возвращает информацию об одном менторе (ваши данные) и шаблонные открытки
        default: Возвращает не тестовые URL's при отсутствии ключа

        Формат использования: python main.py [key] [--token YOUR_TOKEN]
        """
    )

    parser.add_argument(
        "key",
        nargs="?",
        default="default",
        choices=list(URL_CONFIG.keys()),
        help="Ключ для выбора списка URL (по умолчанию: default)"
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Токен бота для запуска (по умолчанию: запускается из .env)"
    )

    args = parser.parse_args()
    urls = URL_CONFIG.get(args.key, URL_CONFIG["default"])

    return (urls[0], urls[1], args.token)
