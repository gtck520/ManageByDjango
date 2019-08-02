from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response

from .serializers import InteractivesSerializer, InteractiveClassSerializer
from .models import Interactives, InteractiveClass
# Create your views here.


class InteractiveClassViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户交互目录
    """
    serializer_class = InteractiveClassSerializer
    queryset = InteractiveClass.objects.all()


class InteractivesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户交互内容
    """
    serializer_class = InteractivesSerializer
    queryset = Interactives.objects.all()

    def list(self, request, *args, **kwargs):
        interclass_id = request.GET.get('class', 1)
        pre_id = request.GET.get('pre', None)   # 默认为第一个问题
        if int(interclass_id) > 0:
            interactives_list = Interactives.objects.filter(interclass=interclass_id, pre_content=pre_id).first()
        else:
            interactives_list = []
        serializer = self.get_serializer(interactives_list)
        return Response(serializer.data)

