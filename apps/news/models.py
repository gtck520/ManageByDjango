# _*_ encoding:utf-8 _*_
from datetime import datetime

from DjangoUeditor.models import UEditorField
from django.db import models

from users.models import UserProfile
# Create your models here.


class ArticleClass(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"类名")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='父类')
    is_hiden = models.BooleanField(default=False, verbose_name=u"是否隐藏")
    keyword = models.CharField(max_length=10, verbose_name=u"类别关键词", null=True, blank=True)
    sort = models.IntegerField( verbose_name=u"排序", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"文章分类"
        verbose_name_plural = verbose_name

    def __str__(self):  # python3用这个方法显示默认查询名称
        return self.name


class Articles(models.Model):
    title = models.CharField(max_length=50, verbose_name=u"标题")
    articleclass = models.ForeignKey(ArticleClass, on_delete=models.CASCADE, verbose_name='分类')
    keyword = models.CharField(max_length=50, verbose_name=u"文章关键字", null=True, blank=True)
    introduction = models.CharField(max_length=200, verbose_name=u"简介", null=True, blank=True)
    image = models.ImageField(upload_to="articles/%Y/%m", verbose_name=u"封面图", max_length=100)
    snap_nums = models.IntegerField(default=0, verbose_name=u"点赞数")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    detail = UEditorField(verbose_name=u"文章详情",width=600, height=300, imagePath="articles/ueditor/",
                          filePath="articles/ueditor/", default='')
    sort = models.IntegerField(verbose_name=u"排序", default=0)
    is_head = models.BooleanField(default=False, verbose_name=u"是否置顶")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u"作者", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now,  verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"文章"
        verbose_name_plural = verbose_name

    def __str__(self):  # python3用这个方法显示默认查询名称
        return self.title