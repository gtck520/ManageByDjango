from django.contrib import admin
import xadmin
# Register your models here.
from xadmin import views
class GlobalSetting(object):
	# 设置后台顶部标题    
	site_title ='我是后台管理呀'
	# 设置后台底部标题    
	site_footer ='我是底部信息啊'
	# 设置菜单可折叠
	menu_style = "accordion"
xadmin.site.register(views.CommAdminView, GlobalSetting)

class BaseSetting(object):
	# 启用主题管理器
	enable_themes =True
	# 使用主题
	use_bootswatch =True
# 注册主题设置
xadmin.site.register(views.BaseAdminView, BaseSetting)