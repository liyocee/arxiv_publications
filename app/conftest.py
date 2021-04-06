import uuid
from typing import Any, Callable, Dict

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from articles.models import Article, Author, Category
from test_utils.utils import random_email, random_lower_string, random_name


@pytest.fixture(scope="module")
def test_password() -> str:
    return 'strong-password'


@pytest.fixture(scope="module")
def user_details() -> Dict[str, str]:
    return {
        'first_name': random_name(),
        'last_name': random_name(),
        'email': random_email(),
        'username': random_lower_string()
    }


@pytest.fixture
def create_user(db: Any, test_password: str) -> Callable[[Dict[str, str]], User]:
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return User.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def user(
    db: Any,
    create_user: Callable[[Dict[str, str]], User],
    user_details: Dict[str, str]
) -> User:
    return create_user(**user_details)


@pytest.fixture
def create_author(db: Any) -> Callable[[], Author]:
    def make_author():
        author = Author.objects.create(
            first_name=random_name(), last_name=random_name()
        )
        return Author.objects.get(last_name=author.last_name)
    return make_author


@pytest.fixture
def author(db: Any, create_author: Callable[[], Author]) -> Author:
    return create_author()


@pytest.fixture
def category(db: Any) -> Category:
    category = Category.objects.create(
        name=random_name(),
        code=random_lower_string(),
        last_sync_date=timezone.now().date()
    )
    return Category.objects.get(code=category.code)


@pytest.fixture
def article(db: Any, category: Category) -> Article:
    article = Article.objects.create(
        created_on=timezone.now().date(),
        updated_on=timezone.now().date(),
        external_id=random_lower_string(),
        summary=random_lower_string(),
        category=category
    )

    return Article.objects.get(external_id=article.external_id)
