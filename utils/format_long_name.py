from libs.api_client.api_requests import Name


def format_long_name(name: Name) -> str:
    if len(name.first) >= 15:
        return f"{' '.join(name.first.split()[:2])}... {name.second}"
    else:
        return name.first+' '+name.second
