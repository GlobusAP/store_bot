def category_check(text: str) -> str:
    return text


def num_check(number: str) -> int:
    if number.isdigit():
        return int(number)
    raise ValueError
