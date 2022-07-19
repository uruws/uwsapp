# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from django.http          import HttpRequest
from django.http          import JsonResponse
from django.views.generic import View

from http import HTTPStatus
from os   import environ

from uwsapp import config
from uwsapp import log

# custom errors

def error404(req: HttpRequest, err: Exception) -> JsonResponse:
	log.debug('error 404:', req)
	log.error(err)
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.NOT_FOUND
	return resp

# ApiView

class ApiView(View):
	http_method_names = ['get', 'head']

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)

# Index

def index(req: HttpRequest) -> JsonResponse:
	log.debug('username:', req.user)
	if config.DEBUG(): return _debug(req)
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.NOT_FOUND
	return resp

def _debug(req: HttpRequest) -> JsonResponse:
	d: dict[str, dict[str, Optional[str]]] = dict(
		environ = dict(),
		headers = dict(),
	)
	for k in sorted(environ.keys()):
		d['environ'][k] = environ.get(k)
	for k in sorted(req.headers.keys()):
		d['headers'][k] = req.headers.get(k)
	resp = JsonResponse(d)
	return resp
