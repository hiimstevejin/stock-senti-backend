from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import NewsArticle
from .serializer import NewsArticleSerializer
from dateutil.parser import parse as parse_date


class NewsArticleListCreate(generics.ListCreateAPIView):
    """
    GET /api/news/
    POST /api/news/
    """
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer


class NewsArticleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/news/<pk>
    PUT /api/news/<pk>
    PATCH /api/news/<pk>
    DELETE /api/news/<pk>
    """
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    lookup_field = "pk"


class CacheNewsView(APIView):
    """
    POST api/news/cache-article/
    api endpoint to receive fetched data from aws Lambda via news api
    """

    def post(self, request):
        data = request.data
        articles = data.get("feed", [])

        for article in articles:
            try:
                time_published = parse_date(article["time_published"])
            except Exception:
                time_published = None

            NewsArticle.objects.update_or_create(
                url=article["url"],
                defaults={
                    "title": article["title"],
                    "time_published": time_published,
                    "authors": article.get("authors", []),
                    "summary": article["summary"],
                    "banner_image": article["banner_image"],
                    "source": article["source"],
                    "overall_sentiment_score": article["overall_sentiment_score"],
                    "overall_sentiment_label": article["overall_sentiment_label"],
                    "topics": article.get("topics", []),
                    "ticker_sentiment": article.get("ticker_sentiment", []),
                },
            )
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
