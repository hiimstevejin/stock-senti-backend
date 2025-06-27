from rest_framework import serializers
from .models import NewsArticle, NewsArticleTopic, NewsArticleTicker


class NewsArticleSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    tickers = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "time_published",
            "authors",
            "summary",
            "banner_image",
            "source",
            "url",
            "overall_sentiment_score",
            "overall_sentiment_label",
            "topics",
            "tickers",
        ]

    def get_topics(self, obj):
        return [
            {
                "name": nt.topic.name,
                "relevance_score": nt.relevance_score,
            }
            for nt in obj.newsarticletopic_set.select_related("topic").all()
        ]

    def get_tickers(self, obj):
        return [
            {
                "symbol": nt.ticker.symbol,
                "sentiment_score": nt.sentiment_score,
                "relevance_score": nt.relevance_score,
                "sentiment_label": nt.sentiment_label,
            }
            for nt in obj.newsarticleticker_set.select_related("ticker").all()
        ]
