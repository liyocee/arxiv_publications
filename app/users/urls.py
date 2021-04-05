
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name="logout"),
    path(
        'article/<int:article_id>/', views.FavouriteArticleView.as_view(),
        name='favourite_article'),
    path(
        'author/<int:author_id>/', views.FavouriteAuthorView.as_view(),
        name='favourite_author'),
]
