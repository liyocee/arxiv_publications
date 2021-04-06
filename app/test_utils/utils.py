import string
import random


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_digits() -> str:
    return "".join(random.choices(string.digits, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_name() -> str:
    return random_lower_string()[:8]
