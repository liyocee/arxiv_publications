from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', include('articles.urls', namespace='articles')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
]
