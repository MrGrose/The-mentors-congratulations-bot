def insert_name(body: str, mentor_name: str) -> str:

    if '#name' in body:
        return body.replace('#name', mentor_name)
    else:
        for i, char in enumerate(body):
            if char.isalpha():
                return body[:i] + ' ' + mentor_name + ', ' + body[i:]
        return mentor_name + ', ' + body
