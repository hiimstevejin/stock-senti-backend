from django.urls import path
from . import views

urlpatterns = [
    path(
        "news/", views.NewsArticleListCreate.as_view(), name="newsarticle-view-create"
    ),
    path(
        "news/<int:pk>", views.NewsArticleRetrieveUpdateDestroy.as_view(), name="update"
    ),
    path("news/cache-article/", views.CacheNewsView.as_view(), name="cache-article"),
]
