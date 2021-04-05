
from typing import Any, Dict
from users.models import UserFavourite

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, ListView

from articles.models import Article, ArticleAuthor, Author


class ArticlesView(ListView):
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 25

    def get_queryset(self) -> QuerySet:
        return Article.objects.all().select_related('category').order_by('-created_on')


class ArticlesDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
    has_favourite = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.has_favourite = UserFavourite.has_favourite(
            self.request.user, self.get_object())
        return super().dispatch(request, *args, **kwargs)


class AuthorArticlesView(ListView):
    template_name = 'author/list.html'
    context_object_name = 'author_articles'
    author = None
    paginate_by = 25

    has_favourite = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.has_favourite = UserFavourite.has_favourite(
            self.request.user, self.get_author())
        return super().dispatch(request, *args, **kwargs)

    def get_author(self):
        if self.author:
            return self.author
        self.author = Author.objects.get(pk=self.kwargs['pk'])
        return self.author

    def get_queryset(self) -> QuerySet:
        author = self.get_author()
        return ArticleAuthor.objects.filter(
            author=author
        ).select_related('article').order_by('-article__created_on')[:20]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data['author'] = self.get_author()
        return context_data
