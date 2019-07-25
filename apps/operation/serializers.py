# -*- coding: utf-8 -*-
# @Time    : 2019/7/21 16:20
# @Author  : konger
# @Site    :
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserComments, UserFavorite, UserSnap
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
    comentslist = serializers.SerializerMethodField('get_coments_list')
    snapid = serializers.SerializerMethodField('get_snap_status')
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

    def get_snap_status(self, obj):
        try:
            snap = UserSnap.objects.filter(snap_type=2, snap_id=obj.id, user=self.context['request'].user).first()
            if snap:
                return snap.id
            else:
                return 0
        except Exception as e:
            print(e)
            return 0


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


class UserSnapSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserSnap
        validators = [
            UniqueTogetherValidator(
                queryset=UserSnap.objects.all(),
                fields=('user', 'snap_id', 'snap_type'),
                message="已经点赞"
            )
        ]

        fields = ('id', 'user', 'snap_id', 'snap_type')
