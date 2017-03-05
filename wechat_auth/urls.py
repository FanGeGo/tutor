#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'youmi'
from django.conf.urls import url
from wechat_auth import views
urlpatterns = [
    url(r'^index', views.index),
    url(r'^login_from_pwd/(?P<id>.*?$)', views.login_from_pwd),
    url(r'^login_admin', views.login_admin),
    # url(r'^loginSuc', views.loginSuc),
    url(r'^authorization', views.authorization),
    url(r'^testjs', views.testJs),
    url(r'^authorizationAdmin', views.authorizationAdmin),
]

import os
from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
    tutor_web = os.path.join(settings.BASE_DIR,'tutor_web')
    admin = os.path.join(settings.BASE_DIR,'Administor')
    urlpatterns += static('/tutor_web/', document_root=tutor_web)
    urlpatterns += static('/administor/', document_root=admin)
