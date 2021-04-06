
from typing import Any, Callable

import pytest
from articles.models import Article, ArticleAuthor, Author, Category
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_retrive_author_articles(
    client: Client,
    category: Category,
    author: Author,
    create_article: Callable[[Any, Category], Callable[[Category], Article]]
):
    article = create_article(category)
    article_author = ArticleAuthor.objects.create(
        author=author,
        article=article
    )
    article_author = ArticleAuthor.objects.get(author=author, article=article)
    url = reverse('articles:author', kwargs={'pk': author.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'author/list.html' in response.template_name
    assert article.title in response.rendered_content
    assert article_author.author.name in response.rendered_content
