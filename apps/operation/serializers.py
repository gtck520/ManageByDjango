# -*- coding: utf-8 -*-
# @Time    : 2019/7/21 16:20
# @Author  : konger
# @Site    :
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from .models import UserComments
from users.serializers import UserDetailSerializer


class UserCommentsSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComments
        fields = "__all__"


class UserCommentsSerializer(serializers.ModelSerializer):
    comentslist = serializers.SerializerMethodField('get_coments_list')   # 文章图片列表 用于前台显示缩略图
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = UserComments
        fields = "__all__"

    def get_coments_list(self, obj):
        try:
            subcoment = UserComments.objects.filter(comment_type=2, comment_id=obj.id)
            if subcoment:
                return subcoment
            else:
                return []
        except Exception as e:
            print(e)
            return []
