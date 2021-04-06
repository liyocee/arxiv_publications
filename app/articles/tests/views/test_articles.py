from typing import Any, Callable

import pytest
from articles.models import Article, ArticleAuthor, Author, Category
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_list_articles(
    client: Client,
    category: Category,
    create_article: Callable[[Any, Category], Callable[[Category], Article]]
):
    article1 = create_article(category)
    article2 = create_article(category)
    url = reverse('articles:index')
    response = client.get(url)
    assert response.status_code == 200
    assert 'articles/list.html' in response.template_name
    assert article1.title in response.rendered_content
    assert article2.title in response.rendered_content


@pytest.mark.django_db
def test_retrive_article(
    client: Client,
    category: Category,
    create_article: Callable[[Any, Category], Callable[[Category], Article]]
):
    article = create_article(category)
    url = reverse('articles:detail', kwargs={'pk': article.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'articles/detail.html' in response.template_name
    assert article.title in response.rendered_content


@pytest.mark.django_db
def test_retrive_article_should_show_authors(
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
    url = reverse('articles:detail', kwargs={'pk': article.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'articles/detail.html' in response.template_name
    assert article.title in response.rendered_content
    assert article_author.author.name in response.rendered_content
