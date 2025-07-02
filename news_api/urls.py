from django.urls import path
from . import views

urlpatterns = [
    path(
        "news/", views.NewsArticleListCreate.as_view(), name="newsarticle-view-create"
    ),
    path(
        "news/<int:pk>", views.NewsArticleRetrieveUpdateDestroy.as_view(), name="update"
    ),
    path("" \
    "news/latest",views.LatestNewsArticlesView.as_view(),name="news-article-get-latests"),
    path(
        "news/topmovers-latest",
        views.TopMoversLatestView.as_view(),
        name="topmovers-get-latests",
    ),
    path("news/cache-article/", views.CacheNewsView.as_view(), name="cache-article"),
    path(
        "news/cache-top-movers/", views.CacheTopMoversView.as_view(), name="top-movers"
    ),
]
