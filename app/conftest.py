from articles.models import Author
import uuid
from django.contrib.auth.models import User
import pytest
from test_utils.utils import (
    random_email, random_name, random_lower_string
)


@pytest.fixture(scope="module")
def test_password():
    return 'strong-password'


@pytest.fixture(scope="module")
def user_details():
    return {
        'first_name': random_name(),
        'last_name': random_name(),
        'email': random_email(),
        'username': random_lower_string()
    }


@pytest.fixture
def create_user(db, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return User.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_author(db):
    def make_author():
        author = Author.objects.create(
            first_name=random_name(), last_name=random_name()
        )
        return Author.objects.get(last_name=author.last_name)
    return make_author
