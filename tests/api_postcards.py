from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Postcard(BaseModel):
    id: int
    holidayId: str
    name_ru: str
    body: str


class DataModel(BaseModel):
    postcards: Optional[list[Postcard]] = None


def read_json_file(filename: str) -> str:
    """Читает JSON файл."""
    with open(f'postcards/{filename}.json', 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()


@app.get("/api/v1/postcards_len_500")
async def get_postcards_len_500():
    """Возвращает открытку с текстом длиннее 500 символов."""
    return Response(content=read_json_file('postcards_len_500'), media_type="application/json")


@app.get("/api/v1/postcards_name_template")
async def get_postcards_name_template():
    """Возвращает открытку с шаблоном для имени."""
    return Response(content=read_json_file('postcards_name_template'), media_type="application/json")


@app.get("/api/v1/postcards_empty_list")
async def get_postcards_empty_list():
    """Возвращает пустой список открыток."""
    return Response(content=read_json_file('postcards_empty_list'), media_type="application/json")


@app.get("/api/v1/postcards_130")
async def get_postcards_130():
    """Возвращает список из 130 открыток."""
    return Response(content=read_json_file('postcards_130'), media_type="application/json")


@app.get("/api/v1/postcards_5")
async def get_postcards_5():
    """Возвращает список из 5 открыток."""
    return Response(content=read_json_file('postcards_5'), media_type="application/json")


@app.get("/api/v1/postcards_invalid")
async def get_postcards_invalid():
    """Возвращает JSON с ошибкой в синтаксисе."""
    return Response(content=read_json_file('postcards_invalid'), media_type="application/json")


@app.get("/api/v1/postcards_not_holidaisid")
async def get_postcards_not_holidaisid():
    """Возвращает данные, не соответствующие схеме (например, отсутствует `holidayId`)."""
    return Response(content=read_json_file('postcards_not_holidaisid'), media_type="application/json")


@app.get("/api/v1/postcards_return_more_data")
async def get_postcards_return_more_data():
    """Возвращает дополнительные данные, не предусмотренные схемой."""
    return Response(content=read_json_file('postcards_return_more_data'), media_type="application/json")
