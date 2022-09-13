# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwslogs URLs"""

from django.urls import path

from .views import Index
from .views import NQ
from .views import NQTail

urlpatterns = [
	path('nq/<slug:jobid>/tail', NQTail.as_view(), name = 'nqlog-tail'),
	path('nq/index',             NQ.as_view(),     name = 'nqlog'),
	path('<slug:name>',          Index.as_view(),  name = 'syslog'),
]
