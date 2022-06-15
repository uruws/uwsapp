# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import HttpRequest
from django.http import JsonResponse

from http       import HTTPStatus
from os         import environ
from pathlib    import Path
from subprocess import check_output

from uwsapp import log

def view(req: HttpRequest, name: str) -> JsonResponse:
	log.debug('username:', req.user)
	log.debug('action:', name)
	resp = None
	if req.method == 'POST':
		try:
			app = req.POST['app']
			resp = _exec(req, name, app)
		except KeyError as err:
			log.error(err)
	if resp is None:
		resp = JsonResponse({})
		resp.status_code = HTTPStatus.BAD_REQUEST
	return resp

def _setenv(user: str):
	e = {}
	for n in ['HOME', 'HOSTNAME', 'PATH', 'USER']:
		e[n] = environ.get(n, '')
	e['NQDIR'] = '/run/uwsapp/nq/%s' % user
	return e

def _check_output(user: str, cmd: str) -> str:
	return check_output(cmd, shell = True, env = _setenv(user)).decode('utf-8')

def _nq(user: str, cmd: str) -> str:
	x = '/usr/bin/nq -- %s' % cmd
	log.debug(x)
	return _check_output(user, x)

def _exec(req: HttpRequest, name: str, app: str) -> JsonResponse:
	user = req.user.username
	log.debug('user:', user)
	cmd = f"/usr/local/bin/apicmd.sh {user} {name} {app}"
	log.debug(cmd)
	try:
		rundir = Path('/run/uwsapp/nq/%s' % user)
		rundir.mkdir(mode = 0o750, parents = True, exist_ok = True)
		resp = JsonResponse({
			'qid': _nq(user, cmd),
		})
	except Exception as err:
		log.error(err)
		resp = JsonResponse({})
		resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
	return resp
