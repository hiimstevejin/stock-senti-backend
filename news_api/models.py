from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    time_published = models.DateTimeField()
    authors = models.JSONField(blank=True, null=True)
    summary = models.TextField()
    banner_image = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=100)
    url = models.URLField()
    overall_sentiment_score = models.FloatField()
    overall_sentiment_label = models.CharField(max_length=50)
    topics = models.JSONField(null=True, blank=True)
    ticker_sentiment = models.JSONField(null=True, blank=True)
    def __str__(self):
        return self.title