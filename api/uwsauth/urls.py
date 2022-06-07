# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwsauth URLs"""

from django.urls import path

from . import views

urlpatterns = [
	path('login', views.login, name='login'),
]
