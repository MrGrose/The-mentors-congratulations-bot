def insert_name(body: str, mentor_name: str) -> str:

    if '#name' in body:
        return body.replace('#name', mentor_name)
    else:
        for num, char in enumerate(body):
            if char.isalpha():
                return body[:num] + ' ' + mentor_name + ', ' + body[num:]
        return mentor_name + ', ' + body
