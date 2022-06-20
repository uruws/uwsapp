# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import HttpRequest
from django.http import JsonResponse

from contextlib import contextmanager
from http       import HTTPStatus
from os         import getenv
from poplib     import POP3_SSL

from uwsapp import log

_hostname: str = 'NOHOSTNAME'
_port:     int = -1
_timeout:  int = 0

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

@contextmanager
def _connect(username: str, password: str) -> POP3_SSL:
	log.debug('username:', username)
	log.debug('hostname:', _hostname, '- port:', _port, '- timeout:', _timeout)
	p = None
	try:
		p = POP3_SSL(_hostname, port = _port, timeout = _timeout)
		p.user(username)
		auth = p.pass_(password)
		log.debug('auth:', username, auth.decode())
		yield p
	finally:
		if p is not None:
			p.quit()

def _badreq() -> JsonResponse:
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.BAD_REQUEST
	return resp

def _unauth() -> JsonResponse:
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.UNAUTHORIZED
	return resp

def index(req: HttpRequest) -> JsonResponse:
	log.debug('req:', req)
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.NOT_FOUND
	return resp

def mbox_list(req: HttpRequest, username: str) -> JsonResponse:
	log.debug('username:', username)
	try:
		password = req.POST['password']
		with _connect(username, password) as pop:
			pass
	except Exception as err:
		log.error(username, 'mbox_list:', err)
		return _unauth()
	return _badreq()
