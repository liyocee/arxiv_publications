import logging

from bs4 import BeautifulSoup
from django.conf import settings
from seeders.seeder import DatabaseSeeder
from articles.models import Category

logger = logging.getLogger(__name__)


class ArticleCategorySeeder(DatabaseSeeder):
    """
    Seed all the article categories from the provided xml file
    """
    DATASOURCE_FILE = settings.BASE_DIR.joinpath(
        'seeders/article_categories/categories.xml'
    )

    def seed(self) -> None:
        logger.info('Seeding Article Categories')
        # from pdb import set_trace; set_trace()

        with open(self.DATASOURCE_FILE) as file:
            parsed_file = BeautifulSoup(file, 'xml')
            category_elements = parsed_file.findAll('set')

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
