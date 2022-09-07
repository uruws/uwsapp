# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwsapps URLs"""

from django.urls import path

from .views import AppInfo
from .views import Index

urlpatterns = [
	path('<slug:name>/info', AppInfo.as_view(), name='app-info'),
	path('',                 Index.as_view(),   name='apps'),
]
