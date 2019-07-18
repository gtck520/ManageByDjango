# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
# 普通分页
from rest_framework.pagination import PageNumberPagination

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


class ContentsSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    经文信息
    """
    serializer_class = ContentsSerializer
    queryset = Contents.objects.all()

    def list(self, request, *args, **kwargs):
        searchstr = kwargs['searchstr']
        content_list = Contents.objects.filter(Lection__contains=searchstr)
        # 实例化产生一个分页对象
        # 不继承来修改对象的值

        # page = PageNumberPagination()
        # page.page_size=2
        # page.page_query_param='bb'

        page = MyPageNumberPagination()
        # 第一个参数:要分页的数据,第二个参数request对象,第三个参数,当前视图对象
        page_list = page.paginate_queryset(content_list, request, self)
        # 再序列化的时候,用分页之后的数据
        serializer = self.get_serializer(instance=page_list, many=True)
        # response['data'] = ser.data
        # return Response(response)
        # 会带着链接,和总共的条数(不建议用)
        return page.get_paginated_response(serializer.data)


# 自定义分页类
class MyPageNumberPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 3
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大页数不超过10
    max_page_size = 10
    # 获取页码数的
    page_query_param = "page"
