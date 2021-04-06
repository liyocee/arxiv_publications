from users.models import UserFavourite
from articles.models import Article
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_user_article_favourting(
    client: Client,
    user: User,
    article: Article, test_password: str
):
    client.login(username=user.username, password=test_password)
    url = reverse('users:favourite_article', kwargs={'article_id': article.id})
    response = client.post(url, {})
    assert response.status_code == 302
    assert UserFavourite.has_favourite(user=user, content_object=article)


@pytest.mark.django_db
def test_user_article_favourting_aunthenticated_user(
    client: Client,
    user: User,
    article: Article, test_password: str
):
    url = reverse('users:favourite_article', kwargs={'article_id': article.id})
    response = client.post(url, {})
    assert '/login/' in response.url
    assert UserFavourite.has_favourite(user=user, content_object=article) is False
