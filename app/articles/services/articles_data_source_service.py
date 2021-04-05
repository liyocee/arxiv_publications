from abc import ABC, abstractclassmethod
from requests import Response


class ArticlesDataSourceService(ABC):

    @abstractclassmethod
    def get_article_categories(self) -> Response:
        raise NotImplementedError

    @abstractclassmethod
    def get_articles(self) -> Response:
        raise NotImplementedError
