from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
# 普通分页
from rest_framework.pagination import PageNumberPagination

from .serializers import ArticleSerializer, ArticleClassSerializer
from .models import Articles, ArticleClass
# Create your views here.


class NewsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    新闻信息
    """
    serializer_class = ArticleSerializer
    queryset = Articles.objects.all()

    def list(self, request, *args, **kwargs):
        content_list = Articles.objects.all()
        # 实例化产生一个分页对象
        # 不继承来修改对象的值

        # page = PageNumberPagination()
        # page.page_size=2
        # page.page_query_param='bb'

        page = MyPageNumberPagination()
        # 第一个参数:要分页的数据,第二个参数request对象,第三个参数,当前视图对象
        page_list = page.paginate_queryset(content_list, request, self)
        # 再序列化的时候,用分页之后的数据 context用于向serializer传参数
        serializer = ArticleSerializer(instance=page_list, many=True, context={'request': request})
        # response['data'] = ser.data
        # return Response(response)
        # 会带着链接,和总共的条数(不建议用)
        return page.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        article.click_nums += 1
        article.save()
        serializer = self.get_serializer(article)
        return Response(serializer.data)


class NewsClassViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    新闻分类
    """
    serializer_class = ArticleClassSerializer
    queryset = ArticleClass.objects.filter(is_hiden=False, parent=None)


# 自定义分页类
class MyPageNumberPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 10
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大页数不超过10
    max_page_size = 10
    # 获取页码数的
    page_query_param = "page"
