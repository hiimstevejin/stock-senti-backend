from django.db import models
from datetime import date


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

    def __str__(self):
        return self.title

class Ticker(models.Model):
    symbol = models.CharField(max_length=10, unique=True, blank=False, null=False)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, default="UNKNOWN")
    industry = models.CharField(
        max_length=100, null=True, blank=True, default="UNKNOWN"
    )
    website = models.URLField(null=True, blank=True)
    market_cap = models.BigIntegerField(null=True)
    headquarters = models.CharField(max_length=100, default="UNKNOWN")

    def __str__(self):
        return self.symbol
    
class Topic(models.Model):
    name = models.CharField(max_length=100, unique= True)

class NewsArticleTopic(models.Model):
    relevance_score = models.FloatField()
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

class NewsArticleTicker(models.Model):
    article = models.ForeignKey(NewsArticle,on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker,on_delete=models.CASCADE)
    sentiment_score=models.FloatField()
    relevance_score=models.FloatField()
    sentiment_label=models.CharField(max_length=50)

class TopGainer(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    price = models.FloatField()
    change_amount = models.FloatField()
    change_percentage = models.CharField(max_length=10)
    volume = models.IntegerField()
    last_updated = models.DateField(default=date.today)

    class Meta:
        unique_together = ("ticker", "last_updated")

    def __str__(self):
        return f"{self.ticker.symbol} gain on {self.last_updated}"


class TopLoser(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    price = models.FloatField()
    change_amount = models.FloatField()
    change_percentage = models.CharField(max_length=10)
    volume = models.IntegerField()
    last_updated = models.DateField(default=date.today)

    class Meta:
        unique_together = ("ticker", "last_updated")

    def __str__(self):
        return f"{self.ticker.symbol} gain on {self.last_updated}"
