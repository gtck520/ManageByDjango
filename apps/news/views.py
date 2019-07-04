from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics

from .serializers import ArticleSerializer
from .models import Articles
# Create your views here.


class NewsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    新闻信息
    """
    serializer_class = ArticleSerializer
    queryset = Articles.objects.all()
