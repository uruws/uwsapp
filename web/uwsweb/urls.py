# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwsweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.contrib      import admin
from django.urls         import include
from django.urls         import path

from uwsapp.config import URL

from .views import Index
from .views import User

from .views_api import Api

from .views_logs import Syslog

from django.contrib.auth.views import LoginView

urlpatterns = [
	path(URL('auth/login'),
		LoginView.as_view(template_name = 'uwsweb/auth/login.html'),
		name = 'login'),

	path(URL('apps/'), include('uwsapps.urls')),

	path(URL('logs/<slug:name>'), Syslog.as_view(), name = 'syslog'),
	path(URL('user'),             User.as_view(),   name = 'user'),
	path(URL('api'),              Api.as_view(),    name = 'api'),

	path(URL('admin/'), admin.site.urls, name = 'admin'),
	path(URL(''),       Index.as_view(), name = 'index'),
]
