# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from django.http import HttpRequest
from django.http import JsonResponse

from contextlib    import contextmanager
from email.message import Message
from email.parser  import BytesParser
from http          import HTTPStatus
from io            import BytesIO
from os            import getenv
from os            import linesep
from poplib        import POP3_SSL

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
def _connect(username: str, password: str):
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

def _msg(m: list[bytes]) -> Message:
	blob = BytesIO()
	for l in m:
		blob.write(l)
		blob.write(linesep.encode())
	blob.seek(0, 0)
	p = BytesParser()
	return p.parse(blob)

def _msg_content(msg):
	c = msg.get_payload(decode = True)
	s = str(c.decode())
	log.debug('parse json')
	return json.loads(s)

def _mlist(username: str, pop: POP3_SSL, l: list[int], lmax: int = 0, indent: int = 0) -> JsonResponse:
	n = 0
	_max = _lmax
	if lmax > 0:
		_max = lmax
	d: dict[str, dict[str, str]] = {}
	try:
		for idx in l:
			m_stat, m_lines, m_size = pop.retr(idx)
			log.debug(m_stat.decode(), len(m_lines), m_size)
			m = _msg(m_lines)
			d[str(idx)] = {
				"date": m['Date'],
				"from": m['From'],
				"subject": m['Subject'],
				"content": _msg_content(m),
			}
			n += 1
			if n >= _max:
				log.print('pop messages list max limit reached:', n)
				break
	except ValueError as err:
		log.error(username, 'mbox_list:', err)
		return _syserror()
	log.debug('MLIST:', len(d), [i for i in d.keys()])
	params = None
	if indent > 0:
		params = {'indent': indent}
	log.debug('json params:', params)
	return JsonResponse(d, json_dumps_params = params)

def mbox_list(req: HttpRequest, username: str) -> JsonResponse:
	"""return list of messages"""
	log.debug('username:', username)
	mlist = []
	try:
		lmax = int(req.POST.get('lmax', _lmax))
		indent = int(req.POST.get('indent', 0))
	except ValueError as err:
		log.debug(username, err)
		lmax = _lmax
		indent = 0
	try:
		password = req.POST['password']
		with _connect(username, password) as pop:
			s, bl, __ = pop.list()
			log.debug('STAT:', s.decode())
			mlist = [int(m.split()[0]) for m in bl]
			return _mlist(username, pop, mlist, lmax = lmax, indent = indent)
	except ValueError as err:
		log.error(username, 'mbox_list:', err)
		return _unauth()
	return _badreq()
