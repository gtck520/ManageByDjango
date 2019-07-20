# -*- coding: utf-8 -*-
# @Time    : 2019/7/4 16:20
# @Author  : konger
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
import re
from rest_framework import serializers
from .models import Articles, ArticleClass

from ManageByDjango.settings import MEDIA_URL


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
    images_list = serializers.SerializerMethodField('get_image_arr')   # 文章图片列表 用于前台显示缩略图
    authorname = serializers.SerializerMethodField('get_author_name')   # 文章作者

    class Meta:
        model = Articles
        fields = "__all__"

    def get_image_arr(self, obj):
        try:
            detail = obj.detail
            reg = r'img src="(.*?)"'  # 定义一个正则来匹配内容中当中的图片
            imgre = re.compile(reg)  # 为了让正则更快，给它来个编译
            # 这个时候做个测试，把匹配的数据都给打印出来
            imglist = re.findall(imgre, detail)  # 通过正则返回所有数据列表
            host = 'http://' + self.context['request'].get_host()
            imglist.append(host+MEDIA_URL+str(obj.image))
            return imglist
        except Exception as e:
            print(e)
            return []

    def get_author_name(self, obj):
        try:
            if obj.author.username:
                authorn = obj.author.username
            else:
                authorn = '本站'
            return authorn
        except Exception as e:
            print(e)
            return '本站'

