# -*- coding: utf-8 -*-
# @Time    : 2019/7/24 22:47
# @Author  : konger
# @Site    :
# @File    : serializers.py
# @Software: PyCharm
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from news.models import Articles
from bible.models import Contents
from .models import UserFavorite, UserSnap, UserComments


@receiver(post_save, sender=UserFavorite)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        fav_id = instance.fav_id
        fav_type = instance.fav_type
        if fav_type == 1:
            article = Articles.objects.get(id=fav_id)
            article.fav_nums += 1
            article.save()
        else:
            a = 1
            # contents = Contents.objects.get(id=fav_id)
            # contents.fav_nums += 1
            # contents.save()


@receiver(post_delete, sender=UserFavorite)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    fav_id = instance.fav_id
    fav_type = instance.fav_type
    if fav_type == 1:
        article = Articles.objects.get(id=fav_id)
        article.fav_nums -= 1
        article.save()
    else:
        a = 1
        # contents = Contents.objects.get(id=fav_id)
        # contents.fav_nums -= 1
        # contents.save()


@receiver(post_save, sender=UserSnap)
def create_usersnap(sender, instance=None, created=False, **kwargs):
    if created:
        snap_id = instance.snap_id
        snap_type = instance.snap_type
        if snap_type == 1:
            article = Articles.objects.get(id=snap_id)
            article.snap_nums += 1
            article.save()
        elif snap_type == 2:
            comment = UserComments.objects.get(id=snap_id)
            comment.snap_nums += 1
            comment.save()
        else:
            a = 1
            # contents = Contents.objects.get(id=fav_id)
            # contents.fav_nums += 1
            # contents.save()


@receiver(post_delete, sender=UserSnap)
def delete_usersnap(sender, instance=None, created=False, **kwargs):
    snap_id = instance.snap_id
    snap_type = instance.snap_type
    if snap_type == 1:
        article = Articles.objects.get(id=snap_id)
        article.snap_nums -= 1
        article.save()
    elif snap_type == 2:
        comment = UserComments.objects.get(id=snap_id)
        comment.snap_nums -= 1
        comment.save()
    else:
        a = 1
        # contents = Contents.objects.get(id=fav_id)
        # contents.fav_nums -= 1
        # contents.save()