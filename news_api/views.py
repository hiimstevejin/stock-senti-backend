from django.shortcuts import render
from rest_framework import generics
from .models import NewsArticle
from .serializer import NewsArticleSerializer


class NewsArticleListCreate(generics.ListCreateAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer


class NewsArticleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    lookup_field = "pk"
