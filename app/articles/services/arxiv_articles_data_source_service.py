
from .articles_data_source_service import ArticlesDataSourceService
from requests import Response
import requests
from django.conf import settings


class ArxivArticlesDataSourceService(ArticlesDataSourceService):

    def get_article_categories(self) -> Response:
        url = settings.ARXIV_BASE_URL + "?verb=ListSets"
        return requests.get(url)
    
    def get_articles(self) -> Response:
        raise NotImplementedError
