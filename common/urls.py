from django.conf.urls import url

from . import views
from .forms import *

APP_NAME = 'common'

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': '%s/login.html' % APP_NAME,'authentication_form':CommonAuthForm}
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': '%s/login.html' % APP_NAME}),
    url(r'^mypage$', views.MyPage.as_view(template_name='%s/mypage.html' % APP_NAME)),
    url(r'^$', views.MyPage.as_view(template_name='%s/mypage.html' % APP_NAME)),
    url(r'^test$', views.MyPage.as_view(template_name='%s/test.html' % APP_NAME)),
]
