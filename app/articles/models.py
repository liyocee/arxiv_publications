import logging
from typing import List, Any

from bs4 import BeautifulSoup
from django.db import models
from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dateutil import parser

logger = logging.getLogger(__name__)


class AbstractBaseModel(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        abstract = True
        ordering = ['-timestamp']


class Category(AbstractBaseModel):
    """
    Article Category
    """
    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True)
    code = models.CharField(
        max_length=255, null=False, blank=False, unique=True,
        help_text='A unique code that identifies the category'
    )
    last_sync_date = models.DateField(null=True, blank=True, default=None)

    def __str__(self) -> str:
        return self.name

    def sync_articles(self, articles_data_fetch_resonse):
        from articles.models import Article
        logging.info(
            f'Syncing articles for category : {self.name} '
            f'with params: {articles_data_fetch_resonse}'
        )
        parsed_response = BeautifulSoup(
            articles_data_fetch_resonse.respone.text,
            features='lxml'
        )
        records = parsed_response.findAll('record')

        for record in records:
            article_external_id = record.find('arxiv').find('id').text

            article = None

            try:
                category = None
                try:
                    category_code = record.find('header').find('setspec').text
                    category = Category.objects.get(code=category_code)
                except Category.DoesNotExist:
                    # Skip over categories we don't recognise
                    continue

                metadata = record.find('arxiv')
                created_on = metadata.find('created').text
                updated_on_element = metadata.find('updated')
                updated_on = (
                    updated_on_element.text if updated_on_element else created_on
                )
                authors = metadata.find('authors').findAll('author')
                title = metadata.find('title').text
                sub_categories = metadata.find('categories').text
                summary = metadata.find('abstract').text
                article = Article.objects.create(
                    created_on=parser.parse(created_on, dayfirst=False),
                    updated_on=parser.parse(updated_on, dayfirst=False),
                    title=title,
                    external_id=article_external_id,
                    summary=summary,
                    category=category
                )
                article.save()
            except IntegrityError:
                article = Article.objects.get(external_id=article_external_id)

            ArticleAuthor.sync_article_authors(
                article=article,
                author_elements=authors
            )

            ArticleSubCategory.sync_article_sub_categories(
                article=article,
                sub_categories=sub_categories
            )

        # Update last sync date
        self.last_sync_date = articles_data_fetch_resonse.end_date
        self.save()

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class SubCategory(AbstractBaseModel):
    """
    Article sub category
    """
    category = models.ForeignKey(
        Category, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(
        max_length=255, null=False, blank=False, unique=True,
        help_text="A unique code that identifies the sub category"
    )

    def __str__(self) -> str:
        return self.name

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')
        unique_together = ('name', 'code')


class Author(AbstractBaseModel):
    last_name = models.CharField(max_length=255, null=False, blank=False)
    first_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}'
    
    @property
    def name(self) -> str:
        return f'{self.last_name} {self.first_name}'

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        unique_together = ('last_name', 'first_name')


class Article(AbstractBaseModel):
    created_on = models.DateField(null=True, blank=True, default=None)
    updated_on = models.DateField(null=True, blank=True, default=None)
    title = models.CharField(max_length=255, null=False, blank=False)
    external_id = models.CharField(
        max_length=255, null=False, blank=False, unique=True,
        help_text="Article identifier in the external source")
    summary = models.TextField(null=False, blank=False)
    category = models.ForeignKey(
        Category, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-updated_on']
        indexes = [
            models.Index(fields=('updated_on',)),
            models.Index(fields=('created_on',)),
        ]


class ArticleAuthor(AbstractBaseModel):
    author = models.ForeignKey(
        Author, null=False, blank=False, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Author: {self.author.name} | Article: {self.article.title}'

    @classmethod
    def sync_article_authors(cls, article: Article, author_elements: List[Any]) -> None:
        for author_element in author_elements:
            first_name = author_element.find('forenames').text
            last_name = author_element.find('keyname').text

            author = None

            try:
                author = Author.objects.create(
                    first_name=first_name,
                    last_name=last_name
                )
                author.save()
            except IntegrityError:
                author = Author.objects.get(
                    first_name=first_name,
                    last_name=last_name
                )

            if author:
                try:
                    author.articleauthor_set.create(article=article)
                except IntegrityError:
                    # the article author already exists
                    pass

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('article_author')
        verbose_name_plural = _('article_authors')
        unique_together = ('article', 'author')


class ArticleSubCategory(AbstractBaseModel):
    article = models.ForeignKey(
        Article, null=False, blank=False, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        SubCategory, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (
            f'SubCategory: {self.sub_category.id} | '
            f'Article: {self.article.id}'
        )

    @classmethod
    def sync_article_sub_categories(
        cls,
        article: Article,
        sub_categories: str
    ) -> None:
        sub_categories_codes = sub_categories.split(' ')

        for sub_category_code in sub_categories_codes:
            try:
                sub_category = SubCategory.objects.get(code=sub_category_code)
                cls.objects.create(
                    article=article,
                    sub_category=sub_category
                )
            except SubCategory.DoesNotExist:
                # Ignore sub categories we cannot recognise
                pass
            except IntegrityError:
                # article subcategory already exists
                pass

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('article_subcategory')
        verbose_name_plural = _('article_subcategories')
        unique_together = ('article', 'sub_category')
