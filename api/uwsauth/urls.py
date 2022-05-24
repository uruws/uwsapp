# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwsauth URLs"""

from django.urls import path
from uwsauth     import views

urlpatterns = [
	path('', views.index, name='auth'),
]
