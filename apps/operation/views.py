from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
# 普通分页
from rest_framework.pagination import PageNumberPagination

from .serializers import UserCommentsSerializer, UserCommentsSubSerializer, UserFavoriteSerializer, UserSnapSerializer\
    , UserInteractivesSerializer, UserInteractivesSerializer1
from .models import UserComments, UserFavorite, UserSnap, UserInteractives
from common.permissions import IsOwnerOrReadOnly
from common import permissions as permissions1
# Create your views here.


class UserCommentsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户评论列表
        可选get参数:
            news 具体评论数据id
            type 评论类型 1 文章 2 评论
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
        comment_type = request.GET.get('type', 1)   # 默认提取文章的所有评论
        if int(news_id) > 0:
            comment_list = UserComments.objects.filter(comment_id=news_id, comment_type=comment_type)
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


class UserFavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取收藏信息
        可选get参数:
            news 具体收藏的数据id
            type 收藏类型 1 文章 2 经文
    create:
        创建收藏
    destroy:
        取消收藏
    """
    # permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserFavoriteSerializer
    queryset = UserFavorite.objects.all()

    def get_permissions(self):
        if self.action == "list":
            return []
        elif self.action == "create" or self.action == "destroy":
            return [permissions.IsAuthenticated(), permissions1.IsOwnerOrReadOnly()]

        return []

    def list(self, request, *args, **kwargs):
        news_id = request.GET.get('news', 0)
        fav_type = request.GET.get('type', 1)   # 默认为文章收藏信息
        if int(news_id) > 0:
            favorite_list = UserFavorite.objects.filter(fav_id=news_id, fav_type=fav_type, user=self.request.user).first()
        else:
            favorite_list = []
        serializer = self.get_serializer(favorite_list)
        return Response(serializer.data)


class UserSnapViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取点赞信息
        可选get参数:
            news 具体收藏的数据id
            type 点赞类型 1 文章 2 评论 3 经文
    create:
        点赞
    destroy:
        取消点赞
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserSnapSerializer
    queryset = UserSnap.objects.all()

    def get_permissions(self):
        if self.action == "list":
            return []
        elif self.action == "create" or self.action == "destroy":
            return [permissions.IsAuthenticated(), permissions1.IsOwnerOrReadOnly()]

        return []

    def list(self, request, *args, **kwargs):
        news_id = request.GET.get('news', 0)
        snap_type = request.GET.get('type', 1)   # 默认为文章收藏信息
        if int(news_id) > 0:
            snap_list = UserSnap.objects.filter(snap_id=news_id, snap_type=snap_type, user=self.request.user).first()
        else:
            snap_list = []
        serializer = self.get_serializer(snap_list)
        return Response(serializer.data)


class UserInteractivesViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                              mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        提取作答信息
        可选get参数:
            user 具体某用户id
            interactives 具体某一问题id
    update:
        修改答案
    create:
        作答
    destroy:
        取消作答
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserInteractivesSerializer
    queryset = UserInteractives.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return UserInteractivesSerializer1
        elif self.action == "create" or self.action == "update":
            return UserInteractivesSerializer

        return UserInteractivesSerializer

    def get_permissions(self):
        if self.action == "list":
            return []
        elif self.action != "list":
            return [permissions.IsAuthenticated(), permissions1.IsOwnerOrReadOnly()]

        return []

    def get_queryset(self):
        if self.action == "list":
            hasdo = self.request.GET.get('hasdo', 0)
            interid = self.request.GET.get('interid', 0)
            if int(hasdo) > 0 or int(interid) > 0:
                if int(hasdo) == 1:
                    if int(interid) > 0:
                        return UserInteractives.objects.filter(has_read=True, interactive=interid).order_by('-id')
                    else:
                        return UserInteractives.objects.filter(has_read=True).order_by('-id')
                else:
                    if int(interid) > 0:
                        return UserInteractives.objects.filter(has_read=False, interactive=interid).order_by('-id')
                    else:
                        return UserInteractives.objects.filter(has_read=False).order_by('-id')
            else:
                return UserInteractives.objects.all().order_by('-id')
        else:
            return UserInteractives.objects.all()


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