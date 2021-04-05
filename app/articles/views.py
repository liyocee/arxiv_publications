
from django.db.models import QuerySet
from django.views.generic import ListView, DetailView

from articles.models import Article


class ArticlesView(ListView):
    template_name = 'articles/list.html'
    context_object_name = 'articles'

    def get_queryset(self) -> QuerySet:
        return Article.objects.all().order_by('-created_on')[: 20]


class ArticlesDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
