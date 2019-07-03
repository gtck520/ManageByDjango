# Register your models here.
import xadmin

from .models import ArticleClass, Articles


class ArticleClassAdmin(object):
    list_display = ['name', 'parent', 'is_hiden', 'keyword', 'sort', 'add_time']
    search_fields = ['name']
    list_filter = [ 'name', 'parent', 'is_hiden', 'add_time']
    model_icon = 'fa fa-university'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('sort',)


class ArticlesAdmin(object):
    list_display = ['title', 'articleclass', 'keyword', 'introduction', 'image', 'click_nums', 'fav_nums', 'detail',
                    'author', 'add_time', 'is_head', 'sort']
    search_fields = ['title', 'introduction', 'keyword', 'detail']
    list_filter = ['click_nums', 'fav_nums', 'articleclass', 'add_time', 'author', 'is_head', 'sort']
    relfield_style = 'fk-ajax'
    model_icon = 'fa fa-university'
    # 设置文章详情使用富文本编辑器
    style_fields = {"detail": "ueditor"}
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('sort',)


xadmin.site.register(ArticleClass, ArticleClassAdmin)
xadmin.site.register(Articles, ArticlesAdmin)
