# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 10:41
# @Author  : konger
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from .models import Books, Contents


class BooksSerializer(serializers.ModelSerializer):
    """
    圣经卷名序列化
    """
    class Meta:
        model = Books
        fields = "__all__"


# 章节
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ("ChapterSN", 'VolumeSN_id')


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ("id", "VerseSN", "ChapterSN", 'VolumeSN_id')


class ContentsSerializer(serializers.ModelSerializer):
    """
    圣经内容
    """
    VolumeSN = BooksSerializer(read_only=True)
    content = serializers.SerializerMethodField('get_search_str')

    class Meta:
        model = Contents
        fields = "__all__"

    def get_search_str(self, obj):
        try:
            searchstr = self.context['searchstr']
            newsearch = '<span class="text-red">' + searchstr + '</span>'
            lectstr = obj.Lection
            lectstr = lectstr.replace(searchstr, newsearch)
            return lectstr
        except Exception as e:
            print(e)
            return []