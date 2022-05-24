# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""CHANGEME URLs"""

from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
]
