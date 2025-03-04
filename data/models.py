from pydantic import BaseModel


class Mentor(BaseModel):
    id: int
    name: str
    tg_username: str
    tg_chat_id: int
    bday: str | None = None

    class Config:
        extra = "ignore"    # Игнорировать дополнительные поля STORY-55


class Postcard(BaseModel):
    id: int
    name: str
    body: str
    holidayId: str | None = None

    class Config:
        extra = "ignore"


class Holiday(BaseModel):
    id: str
    name: str
    name_ru: str

    class Config:
        extra = "ignore"


class ResponseData(BaseModel):
    mentors: list[Mentor] = []
    postcards: list[Postcard] = []
    holidays: list[Holiday] = []

    class Config:
        extra = "ignore"
