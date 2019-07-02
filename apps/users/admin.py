import xadmin
from xadmin import views
# Register your models here.


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "konger后台管理系统"
    site_footer = "测试网"
    menu_style = "accordion"  # 折叠菜单


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)