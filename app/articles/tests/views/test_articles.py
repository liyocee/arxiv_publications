from typing import Any, Callable

import pytest
from articles.models import Article, Category
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_list_articles(
    client: Client,
    category: Category,
    create_article: Callable[[Any, Category], Callable[[Category], Article]]
):
    article1: Article = create_article(category)
    article2: Article = create_article(category)
    url = reverse('articles:index')
    response = client.get(url)
    assert response.status_code == 200
    assert 'articles/list.html' in response.template_name
    assert article1.title in response.rendered_content
    assert article2.title in response.rendered_content
