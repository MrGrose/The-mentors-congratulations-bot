from fastapi import FastAPI, Response

app = FastAPI()


def read_file(path: str) -> str:
    """Читает JSON файл."""
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


@app.get("/mentors_no_items")
async def get_empty_mentors_list():
    """Возвращает пустой список менторов."""
    file_path = "empty_list/mentors_no_items.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/postcards_no_items")
async def get_empty_postcards_list():
    """Возвращает пустой список открыток."""
    file_path = "empty_list/postcards_no_items.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/thirty_mentors")
async def get_large_mentors_list():
    """Возвращает список из 30 менторов."""
    file_path = "large_list/many_mentors.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/postcards_130")
async def get_large_postcards_list():
    """Возвращает список из 130 открыток."""
    file_path = "large_list/many_postcards.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/3_mentors")
async def get_standard_mentors_list():
    """Возвращает список из 3 менторов."""
    file_path = "standard_list/3_mentors.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/postcards_5")
async def get_standard_postcards_list():
    """Возвращает список из 5 открыток."""
    file_path = "standard_list/5_postcards.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/long_name")
async def get_long_name_mentor():
    """Возвращает ментора с именем из 15 слов"""
    file_path = "long_data/long_name.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/long_poscard")
async def get_long_postcard():
    """Возвращает открытку с текстом длиннее 500 символов."""
    file_path = "long_data/long_poscard.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/invalid")
async def get_invalid_json_data():
    """Возвращает JSON с ошибкой."""
    file_path = "invalid_json/mentors_invalid.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/postcards_invalid")
async def get_invalid_postcards_json():
    """Возвращает JSON с ошибкой в синтаксисе."""
    file_path = "invalid_json/postcards_invalid.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/mentors_not_shema")
async def get_mismatched_schema_mentors():
    """Возвращает данные, не соответствующие схеме (например, неправильные типы данных)."""
    file_path = "not_match_scheme/mentors_not_shema.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/postcards_not_shema")
async def get_mismatched_schema_postcards():
    """Возвращает данные, не соответствующие схеме (например, отсутствует `holidayId`)."""
    file_path = "not_match_scheme/postcards_not_shema.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/too_much_mentors")
async def get_excess_data_mentors():
    """Возвращает дополнительные данные, не предусмотренные схемой."""
    file_path = "excess_data/too_much_mentors.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/too_much_postcards")
async def get_excess_data_postcards():
    """Возвращает дополнительные данные, не предусмотренные схемой."""
    file_path = "excess_data/too_much_postcards.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/mentor_info")
async def get_mentor_status():
    """Возвращает информацию об одном менторе (Нужно указать ваши данные)"""
    file_path = "mentor_status/mentor_info.json"
    return Response(content=read_file(file_path), media_type="application/json")


@app.get("/name_template")
async def get_name_template():
    """Возвращает открытку с шаблоном для имени."""
    file_path = "mentor_status/name_template.json"
    return Response(content=read_file(file_path), media_type="application/json")
