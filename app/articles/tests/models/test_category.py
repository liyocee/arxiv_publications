import pytest
from articles.models import Category
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone


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
