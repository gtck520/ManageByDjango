# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from .serializers import BooksSerializer, ChapterSerializer, VerseSerializer, ContentsSerializer
from .models import Books, Contents
# Create your views here.


class BooksViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    卷名信息
    """
    serializer_class = BooksSerializer
    queryset = Books.objects.all()


class ChapterViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    根据卷提供章选信息
    """
    serializer_class = ChapterSerializer
    queryset = Contents.objects.all()

    def list(self, request, *args, **kwargs):
        booksn = kwargs['booksn']
        if booksn:
            # 注意此处有个distinct用法 官方用法distinct('fieldname')  此处mysql用法为 values('ChapterSN').distinct()
            chapters = Contents.objects.filter(VolumeSN_id=booksn).values('ChapterSN').distinct()
            serializer = self.get_serializer(chapters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "卷id不能为空"}, status=status.HTTP_401_UNAUTHORIZED)


class VerseViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    根据章提供节选信息
    """
    serializer_class = VerseSerializer
    queryset = Contents.objects.all()

    def list(self, request, *args, **kwargs):
        booksn = kwargs['booksn']
        chaptersn = kwargs['chaptersn']
        if booksn and chaptersn:
            verse = Contents.objects.filter(VolumeSN_id=booksn, ChapterSN=chaptersn)
            serializer = self.get_serializer(verse, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "卷id与章id不能为空"}, status=status.HTTP_401_UNAUTHORIZED)


class ContentsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    经文信息
    """
    serializer_class = ContentsSerializer
    queryset = Contents.objects.all()

    def list(self, request, *args, **kwargs):
        booksn = kwargs['booksn']
        chaptersn = kwargs['chaptersn']
        if booksn and chaptersn:
            content = Contents.objects.filter(VolumeSN_id=booksn, ChapterSN=chaptersn)
            serializer = self.get_serializer(content, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "卷id与章id不能为空"}, status=status.HTTP_401_UNAUTHORIZED)
