from django.contrib.auth.models import User
from users.models import UserFavourite
from articles.models import Author
from django.test import TestCase
from test_utils.utils import (
    random_email, random_name, random_lower_string
)


class UserFavouriteTestCase(TestCase):
    def setUp(self):
        self.author: Author = Author.objects.create(
            first_name=random_name(), last_name=random_name()
        )
        self.author = Author.objects.get(last_name=self.author.last_name)
        self.user: User = User.objects.create(
            first_name=random_name(),
            last_name=random_name(),
            email=random_email(),
            username=random_lower_string()
        )

    def test_user_has_no_favourite(self):
        user_fav: UserFavourite = UserFavourite.objects.create(
            user=self.user,
            content_object=self.author
        )

        user2: User = User.objects.create(
            first_name=random_name(),
            last_name=random_name(),
            email=random_email(),
            username=random_lower_string()
        )

        self.assertFalse(user_fav.has_favourite(user2, self.author))

    def test_has_favourite(self):
        user_fav: UserFavourite = UserFavourite.objects.create(
            user=self.user,
            content_object=self.author
        )
        self.assertTrue(user_fav.has_favourite(self.user, self.author))
