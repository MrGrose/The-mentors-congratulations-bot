def long_message(text: str) -> list:
    messages = []
    for num in range(0, len(text), 4096):
        messages.append(text[num:num + 4096])
    return messages
