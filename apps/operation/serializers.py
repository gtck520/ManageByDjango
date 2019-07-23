# -*- coding: utf-8 -*-
# @Time    : 2019/7/21 16:20
# @Author  : konger
# @Site    :
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserComments, UserFavorite
from users.serializers import UserDetailSerializer


class UserCommentsSubSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserComments
        fields = "__all__"


class UserCommentsSerializer(serializers.ModelSerializer):
    comentslist = serializers.SerializerMethodField('get_coments_list')   # 文章图片列表 用于前台显示缩略图
    user = UserDetailSerializer(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserComments
        fields = "__all__"

    def get_coments_list(self, obj):
        try:
            subcoment = UserComments.objects.filter(comment_type=2, comment_id=obj.id)
            if subcoment:
                countnum = len(subcoment)
                return {'count': countnum, 'list': subcoment}
            else:
                return {'count': 0}
        except Exception as e:
            print(e)
            return {'count': 0}


class UserFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFavorite
        validators = [
            UniqueTogetherValidator(
                queryset=UserFavorite.objects.all(),
                fields=('user', 'fav_id', 'fav_type'),
                message="已经收藏"
            )
        ]

        fields = ('id', 'user', 'fav_id', 'fav_type')
