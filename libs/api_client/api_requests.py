import httpx

from functools import wraps
from json.decoder import JSONDecodeError
from typing import Any, Callable, List, Optional
from pydantic import BaseModel, ValidationError, Field


class NetworkError(Exception):
    pass


class ResponseFormatError(Exception):
    pass


class ServerError(Exception):
    pass


class Name(BaseModel):
    first: str
    second: str

    class Config:
        extra = "ignore"


class Mentor(BaseModel):
    id: int
    name: Name
    tg_username: str
    tg_chat_id: int
    birthday: Optional[str] = Field(None, alias='bday') 

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True


class MentorData(BaseModel):
    mentors: List[Mentor]

    class Config:
        extra = "ignore"


class Postcard(BaseModel):
    id: int
    holiday_name: str = Field(alias="holidayId")
    name_ru: str
    body: str

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True


class PostcardData(BaseModel):
    postcards: List[Postcard]

    class Config:
        extra = "ignore"


def handle_error_response(func: Callable) -> Callable:
    """Декоратор для обработки ошибок в функциях, работающих с API запросами."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)

        except JSONDecodeError as json_err:
            raise ServerError("Ошибка на стороне сервера: невалидный JSON") from json_err

        except httpx.RequestError as req_err:
            if isinstance(req_err, httpx.ConnectError):
                raise NetworkError(f"Ошибка запроса: {req_err}") from req_err
            else:
                raise ServerError("Ошибка на стороне сервера") from req_err

        except httpx.HTTPStatusError as http_err:
            error_messages = {
                400: "Неправильный запрос",
                401: "Требуется аутентификация",
                403: "Доступ запрещен",
                404: "Ресурс не найден",
            }
            error_message = error_messages.get(http_err.response.status_code, "Неизвестная ошибка")
            raise ServerError(f"Ошибка на стороне сервера: {http_err.response.status_code} - {error_message}") from http_err

        except ValidationError as val_err:
            raise ResponseFormatError("Ошибка формата ответа") from val_err

        except Exception as e:
            raise ServerError("Произошла неизвестная ошибка") from e

    return wrapper


@handle_error_response
def get_postcards(url: str) -> dict[str, Any]:
    """Получает список открыток с сервера."""

    response = httpx.get(url)
    response.raise_for_status()
    validated_data = PostcardData(**response.json())
    return validated_data.model_dump()


@handle_error_response
def get_mentors(url: str) -> dict[str, Any]:
    """Получает список ментеров с сервера."""

    response = httpx.get(url)
    response.raise_for_status()
    validated_data = MentorData(**response.json()) 
    return validated_data.model_dump()
