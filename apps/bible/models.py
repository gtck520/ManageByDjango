# _*_ encoding:utf-8 _*_
from django.db import models

from DjangoUeditor.models import UEditorField
# Create your models here.

class Books(models.Model):
    SN = models.AutoField(max_length=11, verbose_name=u"序号",primary_key=True)
    KindSN = models.IntegerField( verbose_name=u"归类")
    ChapterNumber = models.IntegerField( verbose_name=u"章节数")
    NewOrOld = models.IntegerField(choices=((0, "旧约"), (1, "新约")), default=0, verbose_name=u"新旧约")
    PinYin = models.CharField(max_length=10, verbose_name=u"拼音索引")
    ShortName = models.CharField(max_length=10, verbose_name=u"简称")
    FullName = models.CharField(max_length=20, verbose_name=u"全称")

    class Meta:
        verbose_name = u"圣经卷名"
        verbose_name_plural = verbose_name

    def __unicode__(self):  # python2用这个方法显示默认查询名称
        return self.FullName

    def __str__(self):  # python3用这个方法显示默认查询名称
        return self.FullName


class Contents(models.Model):
    VolumeSN = models.ForeignKey(Books, verbose_name=u"卷名", on_delete=models.CASCADE)
    ChapterSN = models.IntegerField( verbose_name=u"章")
    VerseSN = models.IntegerField( verbose_name=u"节")
    Lection = models.CharField(max_length=255,  verbose_name=u"内容")
    SoundBegin = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=u"语音开始")
    SoundEnd = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=u"语音结束")

    class Meta:
        verbose_name = u"章节内容"
        verbose_name_plural = verbose_name
