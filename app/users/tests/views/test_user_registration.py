from typing import Dict

import pytest
from django.test import Client
from django.urls import reverse
from test_utils.utils import random_name


@pytest.mark.django_db
def test_user_registration_successful(client: Client, user_details: Dict[str, str]):
    url = reverse('users:register')
    payload = user_details
    payload.update({'new_password':  random_name()})
    response = client.post(url, payload)
    assert response.url == reverse('users:login')
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_registration_missing_password(client: Client, user_details: Dict[str, str]):
    url = reverse('users:register')
    payload = user_details
    del payload['username']
    response = client.post(url, payload)
    assert response.status_code == 200
    assert 'users/register.html' in response.template_name
    assert 'This field is required' in response.rendered_content
