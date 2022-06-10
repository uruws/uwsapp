# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse
from os          import environ

from http import HTTPStatus

from uwsapp import config
from uwsapp import log

def index(req):
	if config.DEBUG(): return _debug(req)
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.NOT_FOUND
	return resp

def _debug(req):
	d = dict(
		environ = dict(),
		headers = dict(),
	)
	for k in sorted(environ.keys()):
		d['environ'][k] = environ.get(k)
	for k in sorted(req.headers.keys()):
		d['headers'][k] = req.headers.get(k)
	resp = JsonResponse(d)
	return resp
