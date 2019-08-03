import xadmin
from .models import InteractiveClass, InteractiveMessage, Interactives
# Register your models here.


class InteractiveClassAdmin(object):
    list_display = ['name', 'number', 'score', 'sort', 'add_time']
    search_fields = ['name']
    list_filter = [ 'name', 'add_time']
    model_icon = 'fa fa-tasks'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('sort',)


class InteractiveMessageAdmin(object):
    list_display = ['message', 'message_type', 'show_type', 'add_time']
    search_fields = ['message']
    list_filter = ['message', 'message_type', 'show_type', 'add_time']
    relfield_style = 'fk-ajax'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20


class InteractivesAdmin(object):
    list_display = ['interclass', 'content', 'score', 'content_type', 'pre_content', 'bible_contents',
                    'new_contents', 'add_time',  'sort']
    search_fields = ['content']
    list_filter = ['interclass', 'content', 'score', 'content_type', 'add_time']
    relfield_style = 'fk-ajax'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('sort',)


xadmin.site.register(InteractiveClass, InteractiveClassAdmin)
xadmin.site.register(InteractiveMessage, InteractiveMessageAdmin)
xadmin.site.register(Interactives, InteractivesAdmin)
