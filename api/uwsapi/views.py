# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapp import config

def index(req):
	if config.DEBUG(): return _debug(req)
	resp = JsonResponse(dict())
	resp.status_code = 404
	return resp
