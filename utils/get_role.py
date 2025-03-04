from data.data_fetcher import get_all_data


def start_role(tg_id: str) -> str:
    is_mentor = False
    mentors = get_all_data()
    # print(f'[mentors] {mentors}')
    # TODO: проверка если пустой список
    # TODO: если нет у пользователя @ # AttributeError: 'NoneType' object has no attribute 'lstrip'

    for user in mentors['mentors']:
        tg_username = user.get('tg_username')

        if tg_username is not None and tg_id.lstrip('@') == tg_username.lstrip('@'):
            is_mentor = True
            mentor_name = user.get('name')
            break
    if is_mentor:
        return f"Приветствую ментор: \n{mentor_name}"
    else:
        return f"Приветствую ученик: {tg_id}"
