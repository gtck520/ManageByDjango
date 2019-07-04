from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics

from .serializers import InteractivesSerializer
from .models import Interactives
# Create your views here.


class InteractivesViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户交互内容
    """
    serializer_class = InteractivesSerializer
    queryset = Interactives.objects.all()
