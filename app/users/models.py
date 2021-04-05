from typing import Any

from articles.models import AbstractBaseModel
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserFavourite(AbstractBaseModel):
    user = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return self.user.first_name

    @classmethod
    def has_favourite(cls, user: User, content_object: Any) -> bool:
        if user.is_anonymous:
            return False
        favs = cls.objects.filter(
            object_id=content_object.id,
            content_type=ContentType.objects.get_for_model(content_object),
            user=user
        )
        return favs.exists()

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('user_favourite')
        verbose_name_plural = _('user_favourites')
        unique_together = ('user', 'content_type', 'object_id')
