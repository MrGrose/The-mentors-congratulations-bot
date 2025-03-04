def format_long_name(full_name: str) -> str:
    words = full_name.split()
    if len(words) >= 15:
        first_two_words = ' '.join(words[:2])
        last_two_words = ' '.join(words[-1:])
        return f"{first_two_words}... {last_two_words}"
    else:
        return full_name


def first_name(full_name):
    name = full_name.split()
    if len(name) >= 15:
        return f"{' '.join(name[:2])}..."
    else:
        return name[0]