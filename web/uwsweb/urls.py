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
from django.contrib.auth import views as auth_views
from django.urls         import include
from django.urls         import path

from uwsapp.config import URL

from uwslogs import views as logs_views

from . import views

urlpatterns = [
	path(URL('auth/login'),
		auth_views.LoginView.as_view(template_name = 'uwsweb/auth/login.html'),
		name = 'login'),

	path(URL('logs/'), include('uwslogs.urls')),
	path(URL('apps/'), include('uwsapps.urls')),

	path(URL('user'),   views.User.as_view(), name = 'user'),
	path(URL('api'),    views.Api.as_view(),  name = 'api'),
	path(URL('admin/'), admin.site.urls,      name = 'admin'),

	path(URL(''), logs_views.Index.as_view(), name = 'index'),
]
