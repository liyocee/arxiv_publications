
import logging

import requests
from articles.models import Category
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
from requests import Response

from .articles_data_source_service import (ArticlesDataFetchResponse,
                                           ArticlesDataSourceService)

logger = logging.getLogger(__name__)


class ArxivArticlesDataSourceService(ArticlesDataSourceService):

    def get_article_categories(self) -> Response:
        url = settings.ARXIV_BASE_URL + "?verb=ListSets"
        return requests.get(url)

    def get_articles(
        self, category: Category,
        fetch_interval_days: int
    ) -> ArticlesDataFetchResponse:
        start_date = category.last_sync_date
        url = settings.ARXIV_BASE_URL

        if start_date is None:
            start_date = (
                timezone.now() - relativedelta(
                    months=settings.INITIAL_SYNC_OFFSET_MONTHS)
            ).date()

        end_date = start_date + relativedelta(
            days=+fetch_interval_days
        )

        date_format = '%Y-%m-%d'

        payload = {
            'verb': 'ListRecords',
            'metadataPrefix': 'arXiv',
            'set': category.code,
            'from': start_date.strftime(date_format),
            'until': end_date.strftime(date_format)
        }

        logging.info(
            f'Fetching articles with fetch params: {payload} from url {url}')

        response = requests.post(url, data=payload)
        return ArticlesDataFetchResponse(
            response=response,
            start_date=start_date,
            end_date=end_date
        )
