from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.ArticlesView.as_view(), name='index'),
    path('<int:pk>/', views.ArticlesDetailView.as_view(), name='detail'),
    path('author/<int:pk>/', views.AuthorArticlesView.as_view(), name='author'),
]
