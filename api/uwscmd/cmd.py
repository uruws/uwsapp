# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os         import environ
from pathlib    import Path
from subprocess import CalledProcessError
from subprocess import check_output
from subprocess import STDOUT

from uwsapp import config
from uwsapp import log

__env: dict[str, str] = {
	'PATH':         '/usr/bin:/bin:/usr/local/bin',
	'TZ':           'UTC',
	'HOME':         environ.get('HOME',          ''),
	'HOSTNAME':     environ.get('HOSTNAME',      ''),
	'USER':         environ.get('USER',          ''),
	'UWSAPP_DEBUG': environ.get('UWSAPP_DEBUG',  ''),
	'UWSAPP_HOME':  environ.get('UWSAPP_HOME',   ''),
	'UWSAPP_LOG':   environ.get('UWSAPP_LOG',    ''),
}

def _sshcmd() -> str:
	return config.CLI_SSHCMD().strip()

def _setenv(user: str) -> dict[str, str]:
	e = __env.copy()
	e['UWSAPP_CLI_HOST']   = config.CLI_HOST()
	e['UWSAPP_CLI_SSHCMD'] = _sshcmd()
	e['UWSAPP_USER']       = user
	return e

def _check_output(user: str, cmd: str) -> tuple[str, str]:
	st = 'ok'
	try:
		out = check_output(cmd, stderr = STDOUT, shell = True,
			env = _setenv(user)).decode('utf-8').strip()
	except CalledProcessError as err:
		log.error(err)
		st = 'error'
		out = err.output.decode()
	return (st, out)

def execute(user: str, action: str, app: str, command: str = '') -> dict[str, str]:
	log.debug('user:', user, 'action:', action, 'app:', app)
	cmd = f"/opt/uwsapp/api/libexec/apicmd.sh {user} {action} {app}"
	if command != '':
		cmd = command
	log.debug('cmd:', cmd)
	st, out = _check_output(user, cmd)
	log.debug('status:', st)
	return {'command': cmd, 'output': out, 'status': st}
