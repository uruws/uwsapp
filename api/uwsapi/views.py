# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from django.http import HttpRequest
from django.http import JsonResponse
from os          import environ

from http import HTTPStatus

from uwsapp import config
from uwsapp import log

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

def cmd(req: HttpRequest, name: str) -> JsonResponse:
	resp = JsonResponse(dict())
	return resp
