from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    re_path(r'^test/$', views.testpage, name='test'),
    re_path(r'^home/$', views.home, name='home'),
    # re_path(r'^mall/(\d+)/(\d+)/(\d+)/$', views.mall, name='mall'),
    url(r'^mall/(\d+)/(\d+)/(\d+)/$', views.mall, name='mall'),
    re_path(r'^mall/$', views.mall_redirect, name='mall_redirect'),
    re_path(r'^trolley/$', views.trolley, name='trolley'),
    re_path(r'^profile/$', views.profile, name='profile'),
    # 登录、注册
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^register/$', views.register, name='register'),

]
