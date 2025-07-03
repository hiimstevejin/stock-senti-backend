from datetime import datetime
from django.db import IntegrityError
from django.db.models import Max
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from news_api.permissions import HasInternalAPIKey
from .models import NewsArticle, NewsArticleTopic, Ticker, NewsArticleTicker, TopGainer, TopLoser, Topic
from .serializer import NewsArticleSerializer, TopGainerSerializer, TopLoserSerializer
from dateutil.parser import parse as parse_date


class NewsArticleListCreate(generics.ListCreateAPIView):
    """
    GET /api/news/
    POST /api/news/
    """

    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            return [HasInternalAPIKey()]
        return super().get_permissions()

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

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [HasInternalAPIKey()]
        return super().get_permissions()

class LatestNewsArticlesView(APIView):
    """
    GET /api/news/latest/
    Returns all NewsArticles published on the most recent date
    """
    def get(self, request):
        # Find the max datetime in time_published
        latest_datetime = NewsArticle.objects.aggregate(Max("time_published"))["time_published__max"]
        if not latest_datetime:
            return Response({"news": []}, status=status.HTTP_200_OK)

        # Extract the date portion (ignore time)
        latest_date = latest_datetime.date()

        # Filter articles published on that date (ignoring time)
        articles = NewsArticle.objects.filter(
            time_published__date=latest_date
        ).order_by("-time_published")  # optional ordering newest first

        serializer = NewsArticleSerializer(articles, many=True)
        return Response({"date": latest_date, "news": serializer.data}, status=status.HTTP_200_OK)
    
class TopMoversLatestView(APIView):
    """
    GET /api/news/topmovers-latest
    Returns top gainers and losers for the most recent date
    """

    def get(self, request):
        latest_gainer_date = TopGainer.objects.aggregate(Max('last_updated'))['last_updated__max']
        latest_loser_date = TopLoser.objects.aggregate(Max('last_updated'))['last_updated__max']
        
        valid_dates = list(filter(None, [latest_gainer_date, latest_loser_date]))

        if not valid_dates:
            return Response(
                {"detail": "No data available."},
                status=status.HTTP_200_OK
            )

        latest_date = max(valid_dates)

        top_gainers = TopGainer.objects.filter(last_updated=latest_date)
        top_losers = TopLoser.objects.filter(last_updated=latest_date)

        return Response({
            "date": latest_date,
            "top_gainers": TopGainerSerializer(top_gainers, many=True).data,
            "top_losers": TopLoserSerializer(top_losers, many=True).data,
        })
    
class CacheNewsView(APIView):
    """
    POST api/news/cache-article/
    api endpoint to receive fetched data from aws Lambda via news api
    """
    permission_classes = [HasInternalAPIKey] 
    
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
                ticker_obj, _ = Ticker.objects.get_or_create(
                    symbol=symbol, defaults={"name": symbol}
                )

                try:
                    sentiment_score = float(
                        ticker_entry.get("ticker_sentiment_score", 0)
                    )
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


class CacheTopMoversView(APIView):
    """
    POST /api/top-movers
    Accepts top_gainers and top_losers from news_api
    """

    permission_classes = [HasInternalAPIKey] 

    def post(self, request):
        data = request.data
        top_gainers = data.get("top_gainers", [])
        top_losers = data.get("top_losers", [])
        last_updated_date_str = data.get("last_updated", "").split(" ")[0]
        last_updated = datetime.strptime(last_updated_date_str, "%Y-%m-%d").date()

        inserted_gainers = 0
        inserted_losers = 0

        for gainer in top_gainers:
            symbol = gainer.get("ticker", "").upper()
            if not symbol:
                continue

            ticker_obj, _ = Ticker.objects.get_or_create(
                symbol=symbol, defaults={"name": symbol}
            )

            try:
                TopGainer.objects.create(
                    ticker=ticker_obj,
                    price=float(gainer.get("price", 0)),
                    change_amount=float(gainer.get("change_amount", 0)),
                    change_percentage=gainer.get("change_percentage", "0%"),
                    volume=int(gainer.get("volume", 0)),
                    last_updated=last_updated,
                )
                inserted_gainers += 1
            except IntegrityError as e:
                print(f"Failed to insert {symbol} on {last_updated}: {str(e)}")
                continue  

        for loser in top_losers:
            symbol = loser.get("ticker", "").upper()
            if not symbol:
                continue

            ticker_obj, _ = Ticker.objects.get_or_create(symbol=symbol, defaults={"name": symbol})

            try:
                TopLoser.objects.create(
                    ticker=ticker_obj,
                    price=float(loser.get("price", 0)),
                    change_amount=float(loser.get("change_amount", 0)),
                    change_percentage=loser.get("change_percentage", "0%"),
                    volume=int(loser.get("volume", 0)),
                    last_updated=last_updated,
                )
                inserted_losers += 1
            except IntegrityError as e:
                print(f"Failed to insert {symbol} on {last_updated}: {str(e)}")
                continue  

        return Response(
            {
                "status": "success",
                "inserted_gainers": inserted_gainers,
                "inserted_losers": inserted_losers,
            },
            status=status.HTTP_201_CREATED,
        )
