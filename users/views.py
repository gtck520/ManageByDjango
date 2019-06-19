from django.shortcuts import render

# Create your views here.
# 视图
from  django.contrib.auth.models import User,Group
from  rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from  users.serializers import UserPostSerializer,GroupSerializer,UserSerializer
# Create your views here.

#模型显示的例子
# class UserViewSet(viewsets.ModelViewSet):
#     '''查看，编辑用户的界面'''
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer

# class GroupViewSet(viewsets.ModelViewSet):
#     '''查看，编辑组的界面'''
#     queryset = Group
#     serializer_class = GroupSerializer
class UsersList(viewsets.ModelViewSet):
    """
    注册接口
	-
    主要参数为：
    ----**username:用户名**
    ----**password:密码**
    ----**phone:电话号码**
    ----**code:手机验证码**
    返回参数为：
    其他说明：
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # 定义 GET 请求的方法，内部实现相同 @api_view
    def list(self, request, format=None):
        posts = Post.objects.all()
        serializer = UserSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 定义 POST 请求的方法
    def create(self, requets, format=None):
        serializer_class = UserPostSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

