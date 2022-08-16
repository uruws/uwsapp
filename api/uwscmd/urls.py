# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwscmd URLs"""

from django.urls import path

from .views import Index

urlpatterns = [
	path('<slug:name>', Index.as_view(), name = 'exec'),
]
