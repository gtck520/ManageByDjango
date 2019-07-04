# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserLevel(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"等级名称")
    lowerlimit = models.IntegerField(default=0, verbose_name=u"下限分数")
    upperlimit = models.IntegerField(default=0, verbose_name=u"上限分数")
    feedback = models.IntegerField(default=0, verbose_name=u"反馈贡献")
    contribution = models.IntegerField(default=0, verbose_name=u"获得贡献值")
    add_time = models.DateTimeField(default=datetime.now,  verbose_name=u"添加时间")

    class Meta:
        verbose_name = "用户等级"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class UserProfile(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male",u"男"),("female","女")), default="female")
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)
    score = models.IntegerField(default=0, verbose_name=u"得分")
    level = models.ForeignKey(UserLevel, on_delete=models.CASCADE, null=True, blank=True, verbose_name=u"等级")
    recommend = models.IntegerField(default=0, verbose_name=u"推荐人")
    contribution = models.IntegerField(default=0, verbose_name=u"贡献值")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    #def unread_nums(self):
        # 获取用户未读消息的数量
        #from operation.models import UserMessage
        #return UserMessage.objects.filter(user=self.id, has_read=False).count()


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

