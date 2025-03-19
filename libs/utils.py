from libs.api_client.api_requests import get_mentors


def format_long_name(name: dict) -> str:
    """Форматирует полное имя, сокращая его, если первое имя слишком длинное."""
    first_name = name.get("first")
    last_name = name.get("second")

    if not first_name:
        raise ValueError("Отсутствие имени")

    if len(first_name) >= 15:
        return f"{" ".join(first_name.split()[:2])}... {last_name}"
    else:
        return first_name+" "+last_name


def start_role(chat_id: str, url: str) -> str:
    """Определяет роль пользователя (ментор или ученик) и возвращает приветственное сообщение."""
    is_mentor = False
    mentors = get_mentors(url)
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


def message_splitter(text: str) -> list:
    """Разбивает длинное сообщение на части по 4096 символов."""
    messages = []
    for start_index in range(0, len(text), 4096):
        messages.append(text[start_index:start_index + 4096])
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
        for char_index, char in enumerate(body):
            if char.isalpha():
                return body[:char_index] + " " + mentor_name + ", " + body[char_index:]
        return mentor_name + ", " + body
