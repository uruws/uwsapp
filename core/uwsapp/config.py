# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os           import getenv
from pathlib      import Path
from subprocess   import getoutput
from typing       import Union
from urllib.parse import urljoin

from uwsapp import log

APPNAME = 'app'

# secrets

__unset = '__UNSET__'

__secret_key = getenv('UWSAPP_SECRET', __unset)
if __secret_key is __unset:
	__secret_key = getoutput('/usr/bin/pwgen -1snyB 64').strip()

def SECRET_KEY() -> str:
	return __secret_key

__auth_secret_key = getenv('UWSAPP_AUTH_SECRET', __unset)
if __auth_secret_key is __unset: # pragma: no cover
	__auth_secret_key = 'K0mP2LvwSIPnCI_hyqmEaeRN4_hHiQ1PC_ohAf1J6Eh3FAhD'

def AUTH_SECRET_KEY() -> bytes:
	return __auth_secret_key.encode()

# settings

def _getenv(name: str, default) -> str:
	val = getenv(name, __unset)
	if val is __unset:
		val = str(default)
	return val

def DEBUG() -> bool:
	return _getenv('UWSAPP_DEBUG', 'off') == 'on'

def TESTING() -> bool:
	return _getenv('UWSAPP_TESTING', 'off') == 'on'

def ALLOWED_HOSTS() -> list:
	return [h.strip() for h in _getenv('UWSAPP_HOST', 'localhost').split(',')]

def DBDIR() -> Path:
	return Path(_getenv('UWSAPP_DATADIR', '/var/opt/uwsapp'))

def DBNAME() -> str:
	return _getenv('UWSAPP_DBNAME', '%s.db' % APPNAME)

_url_base = _getenv('UWSAPP_URL', '')

def URL(path: str = '') -> str:
	if _url_base == '':
		return path
	return urljoin(_url_base, path)

def CACHE_CONTROL() -> dict[str, Union[bool, int]]:
	return {
		'max_age':         int(_getenv('UWSAPP_CACHE_MAX_AGE', '5')),
		'must_revalidate': _getenv('UWSAPP_CACHE_REVALIDATE',  'on') == 'on',
		'private':         _getenv('UWSAPP_CACHE_PRIVATE',     'on') == 'on',
		'stale_if_error':  _getenv('UWSAPP_CACHE_ERROR_STALE', 'on') == 'on',
	}

# api

def API_HOST() -> str:
	return _getenv('UWSAPP_API_HOST', 'localhost')

def API_PORT() -> str:
	return _getenv('UWSAPP_API_PORT', '443')

def API_TIMEOUT() -> str:
	return _getenv('UWSAPP_API_TIMEOUT', '15')

def API_CERTFILE() -> str:
	return _getenv('UWSAPP_API_CERTFILE', '')

def API_KEYFILE() -> str:
	return _getenv('UWSAPP_API_KEYFILE', '')

def API_KEYPASS() -> str:
	fn = _getenv('UWSAPP_API_KEYPASS', '/run/uws%s/ca/api_keypass' % APPNAME)
	k = ''
	try:
		k = Path(fn).read_text()
	except Exception as err:
		log.debug('API_KEYPASS:', err)
		k = ''
	return k.strip()

# cli

def CLI_HOST() -> str:
	return _getenv('UWSAPP_CLI_HOST', 'localhost')

def CLI_LOGSDIR() -> Path:
	return Path(_getenv('UWSAPP_CLI_LOGSDIR', '/run/uwscli/logs'))

def CLI_NQDIR() -> Path:
	return Path(_getenv('UWSAPP_CLI_NQDIR', '/run/uwscli/nq'))

def CLI_SSHCMD() -> str:
	return _getenv('UWSAPP_CLI_SSHCMD', '/usr/bin/ssh')
