# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""SKEL URLs"""

from django.urls import path

from .views import Index

urlpatterns = [
	path('/SKEL', Index.as_view(), name='SKEL'),
]
