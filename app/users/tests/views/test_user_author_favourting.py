
import pytest
from articles.models import Author
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from users.models import UserFavourite


@pytest.mark.django_db
def test_user_author_favouriting(
    client: Client,
    user: User,
    author: Author,
    test_password: str
):
    client.login(username=user.username, password=test_password)
    url = reverse('users:favourite_author', kwargs={'author_id': author.id})
    response = client.post(url, {})
    assert response.status_code == 302
    assert UserFavourite.has_favourite(user=user, content_object=author)


@pytest.mark.django_db
def test_user_author_favouriting_aunthenticated_user(
    client: Client,
    user: User,
    author: Author, test_password: str
):
    url = reverse('users:favourite_author', kwargs={'author_id': author.id})
    response = client.post(url, {})
    assert '/login/' in response.url
    assert UserFavourite.has_favourite(user=user, content_object=author) is False
