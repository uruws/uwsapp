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

#
# custom errors
#

def error404(req: HttpRequest, exception: Exception) -> JsonResponse:
	log.debug('error 404:', req)
	log.error(exception)
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.NOT_FOUND
	return resp

#
# ApiView
#

class ApiView(View):
	http_method_names = ['post']

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		log.debug('username:', req.user)

	def uwsapi_resp(v, data, status = HTTPStatus.OK) -> JsonResponse:
		resp = JsonResponse(data)
		resp.status_code = status
		return resp

	def uwsapi_bad_request(v, data = {}) -> JsonResponse:
		resp = JsonResponse(data)
		resp.status_code = HTTPStatus.BAD_REQUEST
		return resp

	def uwsapi_internal_error(v, data = {}) -> JsonResponse:
		resp = JsonResponse(data)
		resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
		return resp

#
# Index
#

class Index(ApiView):
	http_method_names = ['get', 'head']

	def get(v, req, *args, **kwargs) -> JsonResponse:
		if config.DEBUG(): return v._debug(req)
		return v.uwsapi_resp({}, status = HTTPStatus.NOT_FOUND)

	def __debug(v, req: HttpRequest) -> JsonResponse:
		d: dict[str, dict[str, Optional[str]]] = dict(
			environ = dict(),
			headers = dict(),
		)
		for k in sorted(environ.keys()):
			d['environ'][k] = environ.get(k)
		for k in sorted(req.headers.keys()):
			d['headers'][k] = req.headers.get(k)
		return v.uwsapi_resp(d)

#
# Ping
#

class Ping(ApiView):

	def post(v, req) -> JsonResponse:
		return v.uwsapi_resp({"ping": "pong"})
