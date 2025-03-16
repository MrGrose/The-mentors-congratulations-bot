from libs.api_client.api_requests import response_mentors


def format_long_name(name: dict) -> str:
    """Форматирует полное имя, сокращая его, если первое имя слишком длинное."""
    name_first = name.get("first")
    name_second = name.get("second")

    if not name_first:
        raise ValueError("Отсутствие имени")

    if len(name_first) >= 15:
        return f"{" ".join(name_first.split()[:2])}... {name_second}"
    else:
        return name_first+" "+name_second


def start_role(chat_id: str, url: str) -> str:
    """Определяет роль пользователя (ментор или ученик) и возвращает приветственное сообщение."""
    is_mentor = False
    mentors = response_mentors(url)
    if mentors:
        for user in mentors.get("mentors", []):
            if user.get("tg_username") and chat_id.lstrip("@") == user.get("tg_username").lstrip("@"):
                is_mentor = True
                mentor_name = user.get("name").get("first")
                break

    if is_mentor:
        return f"Приветствую ментор: \n{mentor_name}"
    else:
        return f"Приветствую ученик: {chat_id}"


def long_message(text: str) -> list:
    """Разбивает длинное сообщение на части по 4096 символов."""
    messages = []
    for x in range(0, len(text), 4096):
        messages.append(text[x:x + 4096])
    return messages


def insert_name(body: str, mentor_name: str) -> str:
    """
    Вставляет имя ментора в тело сообщения.

    Если в теле сообщения есть метка `#name`, она заменяется именем ментора.
    Иначе имя вставляется перед первым буквенным символом в теле сообщения.
    """
    if "#name" in body:
        return body.replace("#name", mentor_name)
    else:
        for i, char in enumerate(body):
            if char.isalpha():
                return body[:i] + " " + mentor_name + ", " + body[i:]
        return mentor_name + ", " + body
