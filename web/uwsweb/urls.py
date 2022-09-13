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

from .views_apps import Apps
from .views_apps import AppsBuild
from .views_apps import AppBuild
from .views_apps import AppControl
from .views_apps import AppHome

from .views_logs import AppCtl
from .views_logs import NQ
from .views_logs import NQTail
from .views_logs import Uwsq

from django.contrib.auth.views import LoginView

urlpatterns = [
	# auth
	path(URL('auth/login'),
		LoginView.as_view(template_name = 'uwsweb/auth/login.html'),
		name = 'login'),

	# apps
	path(URL('apps/build'),
		AppsBuild.as_view(), name = 'apps-build'),
	path(URL('apps'),
		Apps.as_view(), name = 'apps'),

	# app
	path(URL('app/<slug:name>/build'),
		AppBuild.as_view(), name = 'app-build'),
	path(URL('app/<slug:name>/<slug:action>'),
		AppControl.as_view(), name = 'app-control'),
	path(URL('app/<slug:name>'),
		AppHome.as_view(), name = 'app-home'),

	# logs
	path(URL('logs/nq/<jobid>/tail'), NQTail.as_view(), name = 'nq-logs-tail'),
	path(URL('logs/nq'),              NQ.as_view(),     name = 'nq-logs'),
	path(URL('logs/uwsq'),            Uwsq.as_view(),   name = 'uwsq-logs'),
	path(URL('logs/app-ctl'),         AppCtl.as_view(), name = 'appctl-logs'),

	path(URL('user'), User.as_view(), name = 'user'),
	path(URL('api'),  Api.as_view(),  name = 'api'),

	path(URL('admin/'), admin.site.urls, name = 'admin'),
	path(URL(''),       Index.as_view(), name = 'index'),
]
