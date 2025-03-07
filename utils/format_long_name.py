def format_long_name(full_name: dict) -> str:
    first_name = full_name['first']
    second_name = full_name['second']
    if len(first_name) >= 15:
        return f"{' '.join(first_name.split()[:2])}... {second_name}"
    else:
        return first_name+' '+second_name
