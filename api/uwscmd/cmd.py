# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os         import environ
from pathlib    import Path
from subprocess import check_output

from uwsapp import log

__env: dict[str, str] = {
	'PATH':         '/usr/local/bin:/usr/bin:/bin',
	'HOME':         environ.get('HOME', ''),
	'HOSTNAME':     environ.get('HOSTNAME', ''),
	'USER':         environ.get('USER', ''),
	'UWSAPP_DEBUG': environ.get('UWSAPP_DEBUG', ''),
	'UWSAPP_HOME':  environ.get('UWSAPP_HOME', ''),
	'UWSAPP_LOG':   environ.get('UWSAPP_LOG', ''),
}

def _setenv(user: str) -> dict[str, str]:
	e = __env.copy()
	e['UWSAPP_USER'] = user
	return e

def _check_output(user: str, cmd: str) -> str:
	return check_output(cmd, shell = True, env = _setenv(user)).decode('utf-8').strip()

def execute(user: str, name: str, app: str) -> dict[str, str]:
	log.debug('user:', user)
	cmd = f"/opt/uwsapp/api/libexec/apicmd.sh {user} {name} {app}"
	log.debug(cmd)
	st = 'ok'
	out = _check_output(user, cmd)
	return {'command': cmd, 'output': out, 'status': st}
