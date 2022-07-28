# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwslogs URLs"""

from django.urls import path

from .views import Index
from .views import NQ

urlpatterns = [
	path('nq/<slug:jobid>', NQ.as_view(),    name = 'nqlog'),
	path('<slug:name>',     Index.as_view(), name = 'syslog'),
]
