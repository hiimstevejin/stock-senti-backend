from django.urls import path
from . import views

urlpatterns = [
    path(
        "news/", views.NewsArticleListCreate.as_view(), name="newsarticle-view-create"
    ),
    path(
        "news/<int:pk>", views.NewsArticleRetrieveUpdateDestroy.as_view(), name="update"
    ),
]
