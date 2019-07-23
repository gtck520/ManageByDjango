# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models

from users.models import UserProfile
from interactive.models import Interactives
# Create your models here.


class UserComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"发表用户", on_delete=models.CASCADE)
    comment_id = models.IntegerField(default=0, verbose_name=u"数据id")
    comments = models.CharField(max_length=255, verbose_name=u"评论")
    comment_type = models.IntegerField(choices=((1, "文章"), (2, "评论")), default=1, verbose_name=u"评论类型")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    snap_nums = models.IntegerField(default=0, verbose_name=u"点赞数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    fav_type = models.IntegerField(choices=((1, "文章"), (2, "经文")), default=1, verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ("user", "fav_id", "fav_type")


class UserSnap(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    snap_id = models.IntegerField(default=0, verbose_name=u"数据id")
    snap_type = models.IntegerField(choices=((1, "文章"), (2, "评论"), (3, "经文")), default=1, verbose_name=u"点赞类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户点赞"
        verbose_name_plural = verbose_name


class UserInteractives(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    interactive = models.ForeignKey(Interactives, verbose_name=u"交互内容", on_delete=models.CASCADE)
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户交互"
        verbose_name_plural = verbose_name
