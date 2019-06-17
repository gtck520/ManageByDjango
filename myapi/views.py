from django.shortcuts import render

# Create your views here.
# 视图
from  django.contrib.auth.models import User,Group
from rest_framework import viewsets
from  myapi.serializers import UserSerializer,GroupSerializer
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
class Users(viewsets.ModelViewSet):
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

