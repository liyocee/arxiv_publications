import string
import random

from requests.models import Response


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_digits() -> str:
    return "".join(random.choices(string.digits, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_name() -> str:
    return random_lower_string()[:8]


class MockResponse(Response):

    def __init__(self, status_code: int,  raw_text: str):
        self.status_code = status_code
        self.raw_text = raw_text

    @property
    def text(self):
        return self.raw_text
