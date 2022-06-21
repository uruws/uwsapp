# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import HttpRequest
from django.http import JsonResponse

from contextlib import contextmanager
from http       import HTTPStatus
from os         import getenv
from poplib     import POP3_SSL

from uwsapp import config
from uwsapp import log

_hostname: str = 'localhost'
_port:     int = 995
_timeout:  int = 15
_lmax:     int = 100

def _loadenv():
	"""load config from OS env vars"""
	global _hostname
	global _port
	global _timeout
	global _lmax
	_hostname = getenv('UWSPOP_HOSTNAME', _hostname)
	try:
		_port = int(getenv('UWSPOP_PORT', _port))
		_timeout = int(getenv('UWSPOP_TIMEOUT', _timeout))
		_lmax = int(getenv('UWSPOP_LIST_MAX', _lmax))
	except ValueError as err:
		raise RuntimeError(f"invalid config:", err)

_loadenv()
_debug = config.DEBUG()

@contextmanager
def _connect(username: str, password: str) -> POP3_SSL:
	"""connect to pop3 SSL server and authenticate"""
	log.debug('username:', username)
	log.debug('hostname:', _hostname, '- port:', _port, '- timeout:', _timeout)
	p = None
	try:
		p = POP3_SSL(_hostname, port = _port, timeout = _timeout)
		# ~ if _debug: p.set_debuglevel(1)
		p.user(username)
		auth = p.pass_(password)
		log.print('auth:', username, auth.decode())
		if _debug: log.debug('stat:', p.stat())
		yield p
	finally:
		if p is not None:
			p.quit()

def _syserror() -> JsonResponse:
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
	return resp

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

def _mlist(pop: POP3_SSL, l: list[int]) -> JsonResponse:
	n = 0
	d = {}
	d2 = {}
	try:
		for idx in l:
			d2[str(idx)] = pop.retr(idx)
			n += 1
			if n >= _lmax:
				log.print('pop messages list max limit reached:', n)
				break
	except Exception as err:
		log.error(username, 'mbox_list:', err)
		return _syserror()
	log.debug('MLIST:', len(d2), [i for i in d2.keys()])
	return JsonResponse(d)

def mbox_list(req: HttpRequest, username: str) -> JsonResponse:
	"""return list of messages"""
	log.debug('username:', username)
	mlist = []
	try:
		password = req.POST['password']
		with _connect(username, password) as pop:
			s, bl, __ = pop.list()
			log.debug('STAT:', s.decode())
			mlist = [int(m.split()[0]) for m in bl]
			return _mlist(pop, mlist)
	except Exception as err:
		log.error(username, 'mbox_list:', err)
		return _unauth()
	return _badreq()
