# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""SKEL URLs"""

from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
]
