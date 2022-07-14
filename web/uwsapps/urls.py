# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwsapps URLs"""

from django.urls import path

from . import views

urlpatterns = [
	path('', views.Index.as_view(), name = 'apps'),
]
