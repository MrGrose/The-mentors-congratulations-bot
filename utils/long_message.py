def long_message(text: str) -> list:
    """Разбивает длинное сообщение на части по 4096 символов."""
    messages = []
    for x in range(0, len(text), 4096):
        messages.append(text[x:x + 4096])
    return messages
