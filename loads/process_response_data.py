from loads.models import ResponseData
from pydantic import ValidationError


class NetworkError(Exception):
    pass


class ResponseFormatError(Exception):
    pass


class ServerError(Exception):
    pass


def validate_response_format(response_data):
    try:
        validated_data = ResponseData(**response_data)
        return validated_data.model_dump()
    except ValidationError as val_err:
        raise ResponseFormatError(f"Ошибка формата ответа: {val_err}")


def process_response_data(response_data):

    mentors = []
    postcards = []
    holidays = []

    if isinstance(response_data, dict):
        #  {"mentors": [...], "holidays": [...], "postcards": [...]}
        #  {"mentors": {"mentors": [... ]}, "holidays": {"holidays": [... ]}, "postcards": {"postcards": [... ]}}
        if "mentors" in response_data and isinstance(response_data["mentors"], dict) and "mentors" in response_data["mentors"]:
            mentors = response_data["mentors"]["mentors"]
        elif "mentors" in response_data and isinstance(response_data["mentors"], list):
            mentors = response_data["mentors"]

        if "postcards" in response_data and isinstance(response_data["postcards"], dict) and "postcards" in response_data["postcards"]:
            postcards = response_data["postcards"]["postcards"]
        elif "postcards" in response_data and isinstance(response_data["postcards"], list):
            postcards = response_data["postcards"]

        if "holidays" in response_data and isinstance(response_data["holidays"], dict) and "holidays" in  response_data["holidays"]:
            holidays = response_data["holidays"]["holidays"]
        elif "holidays" in response_data and isinstance(response_data["holidays"], list):
            holidays = response_data["holidays"]

    elif isinstance(response_data, list):
        # Проверка на ключи [{}, {}, {}] 
        for item in response_data:
            if "tg_username" in item:
                mentors.append(item)
            elif "holidayId" in item:
                postcards.append(item)
            elif "name_ru" in item:
                holidays.append(item)
    else:
        raise ResponseFormatError("Неподдерживаемый формат данных: ожидается словарь или список")

    return validate_response_format({"mentors": mentors, "postcards": postcards, "holidays": holidays})