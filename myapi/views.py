from django.shortcuts import render

# Create your views here.
# 视图
from  django.contrib.auth.models import User,Group
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
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
class Register(viewsets.ModelViewSet):
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
    serializer_class = UserSerializer
    
class UserBserDetail(generics.ListCreateAPIView):
	serializer_class = UserSerializer
	def get(self, request, *args, **kwargs):
		user = User.objects.get(pk = kwargs["pk"])
		serializer = UserSerializer(user)
		return Response(serializer.data, status = status.HTTP_201_CREATED)
	def post(self, request, *args, **kwargs):
		serializer = UserSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)