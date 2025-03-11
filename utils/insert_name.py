def insert_name(body: str, mentor_name: str) -> str:
    """
    Вставляет имя ментора в тело сообщения.

    Если в теле сообщения есть метка `#name`, она заменяется именем ментора.
    Иначе имя вставляется перед первым буквенным символом в теле сообщения.
    """
    if '#name' in body:
        return body.replace('#name', mentor_name)
    else:
        for num, char in enumerate(body):
            if char.isalpha():
                return body[:num] + ' ' + mentor_name + ', ' + body[num:]
        return mentor_name + ', ' + body
