import logging
from typing import List

from articles.models import Category
from articles.services.arxiv_articles_data_source_service import \
    ArxivArticlesDataSourceService
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start an initial sync of articles metadata from arxiv'
    requires_migrations_checks = True
    MONTHS_OFFSET_ARG = "months_offset"
    TOPICS_ARG = "topics"

    def __init__(self) -> None:
        super().__init__()
        self.categories = Category.objects.all().order_by('id')
        self._categories_menu = self._get_categories_menu(self.categories)
        print("\n" + self._get_help())

    @staticmethod
    def _get_categories_menu(categories: List[Category]) -> str:
        categories = [f'{cat.id} - {cat.name}' for cat in categories]
        return '\n\t '.join(categories)

    def _get_help(self):
        notice = (
           'Specify months offset with:  `--offset <months>` option.'
           '\nSelect topics from the topics below by '
           ' specifying the `--topic <topic_id>` option from the topics below:'
           f'\n\t {self._categories_menu}'
        )
        return notice

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            f'--{self.MONTHS_OFFSET_ARG}',
            help=(
                'Number of months in the past from which we '
                'should fetch articles metadata'
            ),
        )
        parser.add_argument(
            f'--{self.TOPICS_ARG}',
            help='Select topic_id from the topic list above. i.e 1, 2'
        )

    def handle(self, *args, **options) -> None:
        months_offset = options.get(self.MONTHS_OFFSET_ARG, None)
        if not months_offset:
            months_offset = settings.INITIAL_SYNC_OFFSET_MONTHS

        topics = options.get('topics', '').split(',')
        selected_categories: List[Category] = self.categories.filter(id__in=topics)

        notice = f"""
        \n
        =================================================================
        \n\nArticle sync will happen with offset of {months_offset} months for the
        following topics:
            \n\t {self._get_categories_menu(selected_categories)}
        """
        print(notice)

        data_source_service = ArxivArticlesDataSourceService()

        for selected_category in selected_categories:
            data_source_response = data_source_service.get_articles(
                category=selected_category,
                fetch_interval_days=settings.INITIAL_SYNC_FETCH_INTERVAL_DAYS
            )
            if data_source_response.respone.status_code == 200:
                selected_category.sync_articles(data_source_response)
            else:
                # Todo - handle throttling and now 20x resonses
                logger.error((
                    f'Error fetching articles for category: {selected_category.name} '
                    f'Response: {data_source_response.respone.text}'
                ))
