# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""CHANGEME URLs"""

from django.urls import path

from uwsapp.config import URL

from . import views

urlpatterns = [
	path(URL(''), views.Index.as_view(), name = 'index'),
]
