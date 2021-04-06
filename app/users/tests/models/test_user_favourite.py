from django.contrib.auth.models import User
from users.models import UserFavourite
from test_utils.utils import (
    random_email, random_name
)
import pytest


@pytest.mark.django_db
def test_user_has_no_favourite(create_user, user_details, create_author):
    author = create_author()
    user_fav: UserFavourite = UserFavourite.objects.create(
        user=create_user(**user_details),
        content_object=author
    )

    user2: User = create_user(username=random_name(), email=random_email())

    assert user_fav.has_favourite(user2, author) is False


@pytest.mark.django_db
def test_user_has_favourite(create_user, user_details, create_author):
    author = create_author()
    user = create_user(**user_details)
    user_fav: UserFavourite = UserFavourite.objects.create(
        user=user,
        content_object=author
    )

    assert user_fav.has_favourite(user, author)
