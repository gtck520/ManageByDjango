# -*- coding: utf-8 -*-
# @Time    : 2019/7/4 17:32
# @Author  : konger
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from .models import Interactives, InteractiveMessage, InteractiveClass


class InteractiveClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractiveClass
        fields = "__all__"


class InteractiveMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractiveMessage
        fields = "__all__"


class InteractivesSerializer(serializers.ModelSerializer):
    """
        新闻文章序列化类
    """
    interclass = InteractiveClassSerializer()
    intermessage = InteractiveMessageSerializer()

    class Meta:
        model = Interactives
        fields = "__all__"
