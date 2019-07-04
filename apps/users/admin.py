import xadmin
from xadmin import views

from .models import UserLevel
# Register your models here.


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "konger后台管理系统"
    site_footer = "测试网"
    menu_style = "accordion"  # 折叠菜单


class UserLevelAdmin(object):
    list_display = ['name', 'lowerlimit', 'upperlimit', 'feedback', 'contribution', 'add_time']
    search_fields = ['name']
    list_filter = ['feedback', 'contribution', 'add_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(UserLevel, UserLevelAdmin)