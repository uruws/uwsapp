# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwslogs URLs"""

from django.urls import path

from . import views

urlpatterns = [
	path('', views.Index.as_view(), name = 'index'),
]
