from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserCommentsSerializer, UserCommentsSubSerializer
from .models import UserComments
# 普通分页
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class UserCommentsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户评论列表
    retrieve:
        某条详细评论
    create:
        创建评论
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserCommentsSerializer
    queryset = UserComments.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return UserCommentsSerializer
        elif self.action == "create":
            return UserCommentsSubSerializer

        return UserCommentsSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        elif self.action == "list":
            return []

        return []

    def list(self, request, *args, **kwargs):
        news_id = request.GET.get('news', 0)
        if int(news_id) > 0:
            comment_list = UserComments.objects.filter(comment_id=news_id, comment_type=1)   # 提取文章的所有评论
        else:
            comment_list = []
        page = MyPageNumberPagination()
        # 第一个参数:要分页的数据,第二个参数request对象,第三个参数,当前视图对象
        page_list = page.paginate_queryset(comment_list, request, self)
        # 再序列化的时候,用分页之后的数据 context用于向serializer传参数
        serializer = UserCommentsSerializer(instance=page_list, many=True, context={'request': request})
        # response['data'] = ser.data
        # return Response(response)
        # 会带着链接,和总共的条数(不建议用)
        return page.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        re_dict = serializer.data
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)


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