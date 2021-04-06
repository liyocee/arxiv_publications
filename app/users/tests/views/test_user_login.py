
import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from test_utils.utils import random_lower_string


@pytest.mark.django_db
def test_user_login_successful(client: Client, user: User, test_password: str):
    url = reverse('users:login')
    payload = {
        'username': user.username,
        'password': test_password
    }
    response = client.post(url, payload)
    assert response.status_code == 302
    assert response.url == settings.LOGIN_REDIRECT_URL


@pytest.mark.django_db
def test_user_login_invalid_credentials(client: Client, user: User):
    url = reverse('users:login')
    payload = {
        'username': user.username,
        'password': random_lower_string()
    }
    response = client.post(url, payload)
    assert response.status_code == 200
    assert 'users/login.html' in response.template_name
    assert 'Please enter a correct username and password' in response.rendered_content
