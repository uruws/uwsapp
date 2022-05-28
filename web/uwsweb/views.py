# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import HttpResponse

def index(req):
	return HttpResponse('index')
