"""ManageByDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include  # Django2中的语法
# from django.conf.urls import include, url # Django1.11中的语法
import xadmin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from captcha.views import captcha_refresh

from ManageByDjango.settings import MEDIA_ROOT
from users.views import SmsCodeViewset, UserViewset, UserInfoViewSet, CaptchaViewset, CaptchaCheckViewset
from news.views import NewsViewSet
from interactive.views import InteractivesViewSet
from bible.views import BooksViewSet, ChapterViewset, VerseViewset, ContentsViewSet

router = DefaultRouter()

router.register(r'codes', SmsCodeViewset, base_name="codes")   # 验证码模块
router.register(r'captchas', CaptchaViewset, base_name="captcha")   # 图片验证码
router.register(r'captchas/check', CaptchaCheckViewset, base_name="captcha")   # 图片验证码验证

router.register(r'users', UserViewset, base_name="users")   # 用户模块
router.register(r'userinfo', UserInfoViewSet, base_name="users")   # 用户验证信息模块
router.register(r'news', NewsViewSet, base_name="news")   # 新闻模块
router.register(r'books', BooksViewSet, base_name="books")   # 圣经卷名
router.register(r'books/(?P<booksn>[0-9]+)/chapters', ChapterViewset, base_name="chapters")   # 圣经章选
router.register(r'books/(?P<booksn>[0-9]+)/chapters/(?P<chaptersn>[0-9]+)', VerseViewset, base_name="verses")   # 圣经节选
router.register(r'contents', ContentsViewSet, base_name="contents")   # 经文内容
router.register(r'contents/(?P<booksn>[0-9]+)/(?P<chaptersn>[0-9]+)', ContentsViewSet, base_name="contents")   # 经文
router.register(r'interactives', InteractivesViewSet, base_name="interactives")   # 交互模块


urlpatterns = [
    # path('admin/', admin.site.urls),

    # xadmin后台
    path('admin/', xadmin.site.urls),

    # 注册上面配置的路由
    re_path(r'^v1/', include(router.urls)),

    # 自动化文档
    re_path(r'docs/', include_docs_urls(title="读经")),

    # 自带的权限验证模块
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 富文本编辑器
    path('ueditor/', include('DjangoUeditor.urls')),

    # drf自带的token认证模式
    re_path(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    re_path(r'^login/', obtain_jwt_token),

    # 图片验证码 路由
    path('captcha/', include('captcha.urls')),
]
