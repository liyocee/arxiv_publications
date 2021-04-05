from articles.models import Article, Author
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm
from .models import UserFavourite


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        form.save()
        return redirect(reverse('users:login'))


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class FavouriteArticleView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        article_id = self.kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        favourite = UserFavourite(
            user=self.request.user,
            content_object=article
        )
        try:
            favourite.save()
        except IntegrityError:
            # User has already favourited the article
            pass

        return redirect(reverse('articles:detail', kwargs={'pk': article_id}))


class FavouriteAuthorView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        author = Author.objects.get(id=author_id)
        favourite = UserFavourite(
            user=self.request.user,
            content_object=author
        )
        try:
            favourite.save()
        except IntegrityError:
            # User has already favourited the author
            pass

        return redirect(reverse('articles:author', kwargs={'pk': author_id}))
