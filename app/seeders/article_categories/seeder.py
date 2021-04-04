import logging

from seeders.seeder import DatabaseSeeder

logger = logging.getLogger(__name__)


class ArticleCategorySeeder(DatabaseSeeder):
    """
    Seed all the article categories from the provided xml file
    """

    def seed(self) -> None:
        logger.info("Seeding Article Categories")
