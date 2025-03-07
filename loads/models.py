from pydantic import BaseModel


class Name(BaseModel):
    first: str
    second: str


class Mentor(BaseModel):
    id: int
    name: Name
    tg_username: str
    tg_chat_id: int
    bday: str | None = None

    class Config:
        extra = "ignore"


class Postcard(BaseModel):
    id: int
    name_ru: str | None = None
    body: str
    holidayId: str

    class Config:
        extra = "ignore"


class Holiday(BaseModel):
    id: str
    name: str
    name_ru: str

    class Config:
        extra = "ignore"


class ResponseData(BaseModel):
    mentors: list[Mentor] = None
    postcards: list[Postcard] = None
    holidays: list[Holiday] = None

    class Config:
        extra = "ignore"
