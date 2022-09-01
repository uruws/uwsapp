# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwsapps URLs"""

from django.urls import path

from .views import Index

urlpatterns = [
	path('', Index.as_view(), name='apps'),
]
