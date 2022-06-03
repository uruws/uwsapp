# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse
from os          import environ

from uwsapp import config

def index(req):
	if config.DEBUG(): return _debug(req)
	resp = JsonResponse(dict())
	resp.status_code = 404
	return resp

def _debug(req):
	d = dict()
	for k in sorted(environ.keys()):
		d[k] = environ.get(k)
	resp = JsonResponse(d)
	return resp
