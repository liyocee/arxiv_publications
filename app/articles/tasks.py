from typing import List

from celery import shared_task
from celery.utils.log import get_task_logger

from articles.models import Category
from articles.services.arxiv_articles_data_source_service import \
    ArxivArticlesDataSourceService

logger = get_task_logger(__name__)

data_source_service = ArxivArticlesDataSourceService()


@shared_task
def task_incremental_articles_sync():
    logger.info("Running incremental articles sync")

    """
        - Fetch article categories tosync
        - Categories with the non null `last_sync_date` are the ones that were
          selected during the initial sync. There are the only ones we will be
          incrementally synci'ng
    """
    categories_to_sync: List[Category] = Category.objects.filter(
        last_sync_date__isnull=False)

    for category in categories_to_sync:
        data_source_response = data_source_service.get_articles(
            category=category,
            fetch_interval_days=category.get_sync_interval_days()
        )
        if data_source_response.respone.status_code == 200:
            category.sync_articles(data_source_response)
        else:
            # Todo - handle throttling and now 20x responses
            logger.error((
                f'Error syncing articles for category: {category.name} '
                f'Response: {data_source_response.respone.text}'
            ))
