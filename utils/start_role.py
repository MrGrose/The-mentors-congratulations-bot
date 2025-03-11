from libs.api_client.api_requests import response_mentors


def start_role(chat_id: str) -> str:
    is_mentor = False
    mentors = response_mentors()
    if mentors:
        for user in mentors:
            if user.tg_username and chat_id.lstrip('@') == user.tg_username.lstrip('@'):
                is_mentor = True
                mentor_name = user.name.first
                break

    if is_mentor:
        return f"Приветствую ментор: \n{mentor_name}"
    else:
        return f"Приветствую ученик: {chat_id}"