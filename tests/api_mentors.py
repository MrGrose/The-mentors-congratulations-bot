from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Name(BaseModel):
    first: str
    second: str


class Mentor(BaseModel):
    id: int
    name: Name
    bday: str
    tg_username: str
    tg_chat_id: int


class DataModel(BaseModel):
    mentors: Optional[list[Mentor]] = None


def read_json_file(filename: str) -> str:
    """Читает JSON файл."""
    with open(f'mentors/{filename}.json', 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()



@app.get("/api/v1/empty_list")
async def get_empty_list():
    """Возвращает пустой список менторов."""
    return Response(content=read_json_file('empty_list'), media_type="application/json")


@app.get("/api/v1/thirty_mentors")
async def get_thirty_mentors():
    """Возвращает список из 30 менторов."""
    return Response(content=read_json_file('thirty_mentors'), media_type="application/json")


@app.get("/api/v1/three_mentors")
async def get_three_mentors():
    """Возвращает список из 3 менторов."""
    return Response(content=read_json_file('three_mentors'), media_type="application/json")


@app.get("/api/v1/long_name")
async def get_long_name():
    """Возвращает ментора с именем из 15 слов"""
    return Response(content=read_json_file('long_name'), media_type="application/json")


@app.get("/api/v1/invalid")
async def get_invalid_data():
    """Возвращает JSON с ошибкой."""
    return Response(content=read_json_file('invalid'), media_type="application/json")


@app.get("/api/v1/not_match_schema")
async def get_not_match_schema():
    """Возвращает данные, не соответствующие схеме (например, неправильные типы данных)."""
    return Response(content=read_json_file('not_match_schema'), media_type="application/json")


@app.get("/api/v1/return_more_data")
async def get_return_more_data():
    """Возвращает дополнительные данные, не предусмотренные схемой."""
    return Response(content=read_json_file('return_more_data'), media_type="application/json")


@app.get("/api/v1/i_mentor")
async def get_i_mentor():
    """Возвращает информацию об одном менторе (Нужно указать ваши данные)"""
    return Response(content=read_json_file('i_mentor'), media_type="application/json")