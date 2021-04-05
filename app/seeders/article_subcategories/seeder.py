import logging
from seeders.article_categories.seeder import ArticleCategorySeeder

from bs4 import BeautifulSoup
from django.conf import settings
from seeders.seeder import DatabaseSeeder
from articles.models import Category, SubCategory

logger = logging.getLogger(__name__)


class ArticleSubCategorySeeder(DatabaseSeeder):
    """
    Seed all the article sub categories from the provided html file.
    Sub-categories are retrieved from the "Subject Classifications" table located here:
    https://arxiv.org/help/api/user-manual 
    """
    DATASOURCE_FILE = settings.BASE_DIR.joinpath(
        'seeders/article_subcategories/subcategories.html'
    )

    def seed(self) -> None:
        logger.info('Seeding Article SubCategories')

        # Ensure the categories are seeded first
        article_category_seeder = ArticleCategorySeeder()
        article_category_seeder.seed()

        with open(self.DATASOURCE_FILE) as file:
            parsed_file = BeautifulSoup(file, features='lxml')
            sub_category_elements = parsed_file.find('tbody').findAll('tr')

            for sub_category_element in sub_category_elements:
                elements = sub_category_element.findAll('td')
                sub_category_code = elements[0].text
                sub_category_name = elements[1].text
                category_code = sub_category_code.split(".")[0]

                try:
                    category_record = Category.objects.get(code=category_code)
                    self._create_subcategory(
                        category=category_record,
                        name=sub_category_name,
                        code=sub_category_code)
                except Category.DoesNotExist:
                    continue

    def _create_subcategory(
        self, category: Category, name: str, code: str
    ) -> None:

        try:
            SubCategory.objects.get(code=code, name=name)
        except SubCategory.DoesNotExist:
            SubCategory.objects.create(
                category=category,
                name=name,
                code=code
            )
