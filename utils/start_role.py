from loads.response_data import response_data


def start_role(chat_id: str) -> str:
    is_mentor = False
    mentors_data = response_data()

    if isinstance(mentors_data, dict):
        mentors = (
            mentors_data.get("mentors", {}).get("mentors")
            if "mentors" in mentors_data.get("mentors", {})
            else mentors_data.get("mentors", {})
        )

        if mentors:
            for user in mentors:
                tg_username = user.get("tg_username")
                if tg_username is not None and chat_id.lstrip('@') == tg_username.lstrip('@'):
                    is_mentor = True
                    name = user.get("name")
                    if isinstance(name, dict):
                        mentor_name = name.get("first", "Mentor")
                    else:
                        mentor_name = "Mentor"
                    break

    if is_mentor:
        return f"Приветствую ментор: \n{mentor_name}"
    else:
        return f"Приветствую ученик: {chat_id}"