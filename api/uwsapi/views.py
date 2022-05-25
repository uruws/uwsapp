# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

def index(req):
	resp = JsonResponse(dict())
	resp.status_code = 404
	return resp
