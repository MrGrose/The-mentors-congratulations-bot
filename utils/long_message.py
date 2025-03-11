def long_message(text: str) -> list:
    messages = []
    for x in range(0, len(text), 4096):
        messages.append(text[x:x + 4096])
    return messages
