# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""CHANGEME URLs"""

from django.urls import path

from uwsapp.config import URL

from . import views

urlpatterns = [
	path('<path:path>', views.Help.as_view(), name = 'help'),
	path('', views.Index.as_view(), name = 'help-index'),
]
