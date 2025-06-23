from rest_framework import serializers
from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
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
            "ticker_sentiment",
        ]
