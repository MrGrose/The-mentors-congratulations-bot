import httpx
# import json
from functools import lru_cache
from data.models import ResponseData


class NetworkError(Exception):
    pass


class ResponseFormatError(Exception):
    pass


def validate_response_format(response_data):
    try:
        validated_data = ResponseData(**response_data)
        return validated_data.model_dump()
    except Exception as e:
        raise ResponseFormatError(f"Ошибка формата ответа: {e}")


# TODO: Валидация url?

# @lru_cache(maxsize=1)
def get_all_data(name: str = None, url: str = None) -> dict:

    # url = 'http://127.0.0.1:8002/api/v1/test2'
    url = 'http://127.0.0.1:8001/api/v1/mentors'
    # url = 'http://127.0.0.1:8000/mentor_long_name'
    # url = 'http://127.0.0.1:8000/test2'
    # url = 'http://127.0.0.1:8000/mentors'
    # url = 'http://127.0.0.1:8000/three_mentors'
    # url = 'http://127.0.0.1:8000/double_mentors'
    # url = 'http://127.0.0.1:8002/hb'
    try:
        response = httpx.get(url)
        response.raise_for_status()
        response_data = response.json()

        # try:
        #     response_data = response.json()
        # except json.JSONDecodeError as e:           # Проверка на невалидный json
        #     print(f"Ошибка парсинга JSON: {e}")
        #     return []

        if not isinstance(response_data, (dict, list)):
            raise ResponseFormatError("Ответ должен быть словарем или списком")

        if isinstance(response_data, list):
            if not response_data:
                return {
                    "mentors_list": [],
                    "postcards_list": [],
                    "holidays_list": []
                }
            else:
                if "date" in response_data[0]:           # поле "date", открытки
                    response_data = {"postcards": response_data}
                elif "tg_username" in response_data[0]:  # поле "tg_username", наставники
                    response_data = {"mentors": response_data}
                elif "id" in response_data[0]:           # поле "id", праздники
                    response_data = {"holidays": response_data}
                else:
                    raise ResponseFormatError("Неправильный формат данных")

        validated_data = validate_response_format(response_data)

        if name:
            return {
                f"{name}_list": validated_data.get(name, [])
            }
        else:
            return validated_data

    except httpx.RequestError as req_err:
        raise NetworkError(f"Ошибка запроса: {req_err}")
    except httpx.HTTPStatusError as http_err:
        error_messages = {
            400: "Неправильный запрос",
            401: "Требуется аутентификация",
            403: "Доступ запрещен",
            404: "Ресурс не найден",
        }
        if http_err.response.status_code >= 500:
            print(f"Ошибка {http_err.response.status_code}: Ошибка на стороне сервера")
        elif http_err.response.status_code in error_messages:
            print(f"Ошибка {http_err.response.status_code}: {error_messages[http_err.response.status_code]}")
        return []
    except ResponseFormatError as format_err:
        print(f"Ошибка формата ответа: {format_err}")
        return []
    except Exception as e:
        print(f"Какая-то общая ошибка: {e}")
        return []

# get_all_data.cache_clear()
