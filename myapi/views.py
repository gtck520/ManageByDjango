from django.shortcuts import render

# Create your views here.
# 视图
from  django.contrib.auth.models import User,Group
from rest_framework import viewsets
from  myapi.serializers import UserSerializer,GroupSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    '''查看，编辑用户的界面'''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    '''查看，编辑组的界面'''
    queryset = Group
    serializer_class = GroupSerializer