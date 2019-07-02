from django.contrib import admin

# Register your models here.
import xadmin
from .models import Books, Contents


class BooksAdmin(object):
    list_display = ['SN', 'KindSN', 'ChapterNumber', 'NewOrOld', 'PinYin', 'ShortName', 'FullName']
    search_fields = ['PinYin', 'ShortName', 'FullName']
    list_filter = [ 'KindSN', 'ChapterNumber', 'NewOrOld', 'PinYin', 'ShortName', 'FullName']
    model_icon = 'fa fa-university'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('SN',)


class ContentsAdmin(object):
    list_display = ['VolumeSN', 'ChapterSN', 'VerseSN', 'Lection', 'SoundBegin', 'SoundEnd']
    search_fields = ['Lection','VolumeSN__FullName']
    list_filter = ['VolumeSN', 'ChapterSN', 'VerseSN', 'Lection']
    relfield_style = 'fk-ajax'
    model_icon = 'fa fa-university'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)


xadmin.site.register(Books, BooksAdmin)
xadmin.site.register(Contents, ContentsAdmin)