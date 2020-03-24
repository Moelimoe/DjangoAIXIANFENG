from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    re_path(r'^test/$', views.testpage, name='test'),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    re_path(r'^mall/(\d+)/(\d+)/(\d+)/$', views.mall, name='mall'),
    re_path(r'^mall/$', views.mall_redirect, name='mall_redirect'),
    re_path(r'^trolley/$', views.trolley, name='trolley'),
    re_path(r'^profile/$', views.profile, name='profile'),
    # 登录、注册
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^register/$', views.register, name='register'),
    # 检查用户注册id是否已存在
    re_path(r'^checkuserid/$', views.checkuserid, name='checkuserid'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^signout/$', views.signout, name='signout'),
    # 修改购物车信息
    re_path(r'^changetrolley/(\d+)/$', views.changetrolley, name='changetrolley'),
    # 提交订单
    re_path(r'^submitorder/$', views.submitorder, name='submitorder'),
    # 验证码
    re_path(r'^captcha/$', views.captcha, name='captcha'),
]

# 实现登录、注册或进入个人资料时展示头像
urlpatterns += static('/login/', document_root=settings.MEDIA_ROOT)
urlpatterns += static('/profile/', document_root=settings.MEDIA_ROOT)
urlpatterns += static('/register/', document_root=settings.MEDIA_ROOT)


# 测试页
urlpatterns += static('/test/', document_root=settings.MEDIA_ROOT)
