# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import HttpRequest
from django.http import JsonResponse

from http import HTTPStatus

from uwsapp import log

def view(req: HttpRequest, name: str) -> JsonResponse:
	log.debug('username:', req.user)
	log.debug('action:', name)
	if req.method == 'POST':
		try:
			app = req.POST['app']
		except KeyError as err:
			log.error(err)
		return _exec(req, name, app)
	resp = JsonResponse({})
	resp.status_code = HTTPStatus.BAD_REQUEST
	return resp

def _exec(req: HttpRequest, name: str, app: str) -> JsonResponse:
	resp = JsonResponse({})
	resp.status_code = HTTPStatus.BAD_REQUEST
	return resp
