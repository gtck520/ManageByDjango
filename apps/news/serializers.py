# -*- coding: utf-8 -*-
# @Time    : 2019/7/4 16:20
# @Author  : konger
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers
from .models import Articles, ArticleClass


class ArticleClassSerializer3(serializers.ModelSerializer):

    class Meta:
        model = ArticleClass
        fields = "__all__"


class ArticleClassSerializer2(serializers.ModelSerializer):
    subs = ArticleClassSerializer3(many=True)

    class Meta:
        model = ArticleClass
        fields = "__all__"


class ArticleClassSerializer(serializers.ModelSerializer):
    subs = ArticleClassSerializer2(many=True)

    class Meta:
        model = ArticleClass
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    """
        新闻文章序列化类
    """
    articleclass = ArticleClassSerializer()

    class Meta:
        model = Articles
        fields = "__all__"
