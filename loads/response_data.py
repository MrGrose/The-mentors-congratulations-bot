import httpx
from json.decoder import JSONDecodeError
from loads.process_response_data import process_response_data


class NetworkError(Exception):
    pass


class ResponseFormatError(Exception):
    pass


class ServerError(Exception):
    pass


def response_data(name: str = None) -> dict:
    url = 'https://my-json-server.typicode.com/devmanorg/congrats-mentor/holidays'
    try:
        response = httpx.get(url)
        response.raise_for_status()
        processed = response.json()
        processed_data = process_response_data(processed)

        if name:
            return {f"{name}": processed_data.get(name, [])}
        else:
            return processed_data

    except JSONDecodeError as json_err:
        print(f"Ошибка парсинга JSON: {json_err}")
        raise ServerError("Ошибка на стороне сервера: невалидный JSON") from json_err

    except httpx.RequestError as req_err:
        if isinstance(req_err, httpx.ConnectError):
            raise NetworkError(f"Ошибка запроса: {req_err}") from req_err
        else:
            print(f"Ошибка на стороне сервера: {req_err}")
            raise ServerError("Ошибка на стороне сервера") from req_err

    except httpx.HTTPStatusError as http_err:
        error_messages = {
            400: "Неправильный запрос",
            401: "Требуется аутентификация",
            403: "Доступ запрещен",
            404: "Ресурс не найден",
        }
        error_message = error_messages.get(http_err.response.status_code, "Неизвестная ошибка")
        print(f"Ошибка HTTP: {http_err.response.status_code} - {error_message}")
        raise ServerError(f"Ошибка на стороне сервера: {http_err.response.status_code} - {error_message}") from http_err

    except ResponseFormatError as format_err:
        print(f"Ошибка формата ответа: {format_err}")
        return {}

    except ServerError as server_err:
        print(f"Ошибка сервера: {server_err}")
        return {}

    except Exception as e:
        print(f"Какая-то общая ошибка: {e}")
        return {}
