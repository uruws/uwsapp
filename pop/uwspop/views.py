# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import HttpRequest
from django.http import JsonResponse

from http   import HTTPStatus
from os     import getenv
from poplib import POP3_SSL

from uwsapp import log

_hostname: str = 'NOHOSTNAME'
_port:     int = -1
_timeout:  int = -1

def _loadenv():
	global _hostname
	global _port
	global _timeout
	_hostname = getenv('UWSPOP_HOSTNAME', 'localhost')
	try:
		_port = int(getenv('UWSPOP_PORT', 995))
		_timeout = int(getenv('UWSPOP_TIMEOUT', 15))
	except ValueError as err:
		raise RuntimeError(f"UWSPOP_PORT: invalid setting:", err)

_loadenv()

def _connect(username: str, password: str) -> POP3_SSL:
	return POP3_SSL(_hostname, port = _port, timeout = _timeout)

def index(req: HttpRequest) -> JsonResponse:
	log.debug('req:', req)
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.NOT_FOUND
	return resp
