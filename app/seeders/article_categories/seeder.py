import logging

from bs4 import BeautifulSoup
from seeders.seeder import DatabaseSeeder
from articles.models import Category
from articles.services.arxiv_articles_data_source_service import (
    ArxivArticlesDataSourceService
)


logger = logging.getLogger(__name__)


class ArticleCategorySeeder(DatabaseSeeder):
    """
    Seed all the article categories from the provided `ListSets`
    """
    def __init__(self) -> None:
        self.data_rouce = ArxivArticlesDataSourceService()

    def seed(self) -> None:
        logger.info('Seeding Article Categories')
        response = self.data_rouce.get_article_categories()
        parsed_response = BeautifulSoup(response.text, 'xml')
        category_elements = parsed_response.findAll('set')

        for category_element in category_elements:
            category_name = category_element.setName.text
            category_code = category_element.setSpec.text

            try:
                Category.objects.get(code=category_code)
            except Category.DoesNotExist:
                Category.objects.create(
                    name=category_name,
                    code=category_code
                )
