# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

def index(req):
	return JsonResponse(dict(testing = 'test0'))
