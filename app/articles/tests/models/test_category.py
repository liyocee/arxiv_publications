from pathlib import Path

import pytest
from articles.models import Article, Category
from articles.services.articles_data_source_service import \
    ArticlesDataFetchResponse
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
from test_utils.utils import MockResponse


@pytest.mark.django_db
def test_get_sync_interval_days_without_initial_sync(category: Category):
    category.last_sync_date = None
    category.save()
    assert (
        category.get_sync_interval_days() == settings.INITIAL_SYNC_FETCH_INTERVAL_DAYS
    )


@pytest.mark.django_db
def test_get_sync_interval_days_sync_lag_less_than_initial_interval(category: Category):
    now = timezone.now().date()
    small_sync_lag = settings.INITIAL_SYNC_FETCH_INTERVAL_DAYS - 1
    sync_lag_delta = relativedelta(days=small_sync_lag)
    category.last_sync_date = now - sync_lag_delta
    category.save()
    expected_interval = now - category.last_sync_date
    assert (
        category.get_sync_interval_days() == expected_interval.days
    )


@pytest.mark.django_db
def test_get_sync_interval_days_sync_lag_more_than_initial_interval(category: Category):
    now = timezone.now().date()
    big_sync_lag = settings.INITIAL_SYNC_FETCH_INTERVAL_DAYS + 10
    sync_lag_delta = relativedelta(days=big_sync_lag)
    category.last_sync_date = now - sync_lag_delta
    category.save()

    assert (
        category.get_sync_interval_days() == settings.INITIAL_SYNC_FETCH_INTERVAL_DAYS
    )


@pytest.mark.django_db(transaction=True)
def test_sync_articles(category: Category):
    category_code = 'q-bio'
    category.code = category_code
    category.last_sync_date = None
    category.save()
    articles_response_file = (
        Path(__file__).resolve().parent.joinpath('fetch_articles_response.xml')
    )

    end_date = timezone.now().date()
    start_date = end_date + relativedelta(days=20)

    with open(articles_response_file) as fyl:
        articles_response = fyl.read()
        data_fetch_response = ArticlesDataFetchResponse(
            response=MockResponse(status_code=200, raw_text=articles_response),
            start_date=start_date,
            end_date=end_date
        )
        category.sync_articles(data_fetch_response)
        parsed_response = BeautifulSoup(
           articles_response,
           features='lxml'
        )
        record = parsed_response.findAll('record')[0]
        article_external_id = record.find('arxiv').find('id').text

        articles = Article.objects.filter(external_id=article_external_id) 
        assert len(articles) == 1
