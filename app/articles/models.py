from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
        max_length=255, null=False, blank=False,
        help_text="A unique code that identifies the sub category"
    )

    def __str__(self) -> str:
        return self.name

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')
        unique_together = ('name', 'code')


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


class Author(AbstractBaseModel):
    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class ArticleAuthor(AbstractBaseModel):
    author = models.ForeignKey(
        Author, null=False, blank=False, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Author: {self.author.name} | Article: {self.article.title}'

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

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('article_subcategory')
        verbose_name_plural = _('article_subcategories')
        unique_together = ('article', 'sub_category')
