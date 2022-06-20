# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import HttpRequest
from django.http import JsonResponse
from http        import HTTPStatus

from uwsapp import log

def index(req: HttpRequest) -> JsonResponse:
	log.debug('req:', req)
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.NOT_FOUND
	return resp
