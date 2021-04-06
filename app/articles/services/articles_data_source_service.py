from abc import ABC, abstractclassmethod

from articles.models import Category
from requests import Response
from datetime import date


class ArticlesDataFetchResponse:
    def __init__(self, response: Response, start_date: date, end_date: date) -> None:
        self.respone = response
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self) -> str:
        return (
            f'StartDate: {self.start_date} '
            f'EndDate: {self.start_date} '
        )


class ArticlesDataSourceService(ABC):

    @abstractclassmethod
    def get_article_categories(self) -> Response:
        raise NotImplementedError

    @abstractclassmethod
    def get_articles(
        self,
        category: Category,
        fetch_interval_days: int
    ) -> ArticlesDataFetchResponse:
        raise NotImplementedError
