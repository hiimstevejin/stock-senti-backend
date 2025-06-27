from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import NewsArticle, NewsArticleTopic, Ticker, NewsArticleTicker, Topic
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

            news_article, created = NewsArticle.objects.update_or_create(
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
                },
            )

            for topic_entry in article.get("topics", []):
                topic_name = topic_entry.get("topic")

                if topic_name:
                    topic_obj, _ = Topic.objects.get_or_create(name=topic_name)
                    try:
                        relevance_score = float(topic_entry.get("relevance_score", 0))
                    except (ValueError, TypeError):
                        relevance_score = 0.0

                    NewsArticleTopic.objects.update_or_create(
                        article=news_article,
                        topic=topic_obj,
                        defaults={"relevance_score": relevance_score},
                    )

            for ticker_entry in article.get("ticker_sentiment", []):
                symbol = ticker_entry.get("ticker", "").upper()
                if not symbol:
                    continue
                ticker_obj, _ = Ticker.objects.get_or_create(symbol=symbol, defaults={"name": symbol})

                try:
                    sentiment_score = float(ticker_entry.get("ticker_sentiment_score", 0))
                except (ValueError, TypeError):
                    sentiment_score = 0.0

                try:
                    relevance_score = float(ticker_entry.get("relevance_score", 0))
                except (ValueError, TypeError):
                    relevance_score = 0.0

                sentiment_label = ticker_entry.get("ticker_sentiment_label", "")

                NewsArticleTicker.objects.update_or_create(
                    article=news_article,
                    ticker=ticker_obj,
                    defaults={
                        "sentiment_score": sentiment_score,
                        "relevance_score": relevance_score,
                        "sentiment_label": sentiment_label,
                    },
                )

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
