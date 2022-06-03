# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os           import getenv
from pathlib      import Path
from subprocess   import getoutput
from urllib.parse import urljoin

APPNAME = 'app'

__unset = '__UNSET__'

__secret_key = getenv('UWSAPP_SECRET', __unset)
if __secret_key is __unset:
	__secret_key = getoutput('/usr/bin/pwgen -1snyB 64')

def SECRET_KEY() -> str:
	return __secret_key

def _getenv(name: str, default) -> str:
	val = getenv(name, __unset)
	if val is __unset:
		val = str(default)
	return val

def DEBUG() -> bool:
	return _getenv('UWSAPP_DEBUG', 'off') == 'on'

def ALLOWED_HOSTS() -> list:
	if DEBUG(): return []
	return [_getenv('UWSAPP_HOST', 'localhost')]

def DBDIR() -> Path:
	return Path(_getenv('UWSAPP_DATADIR', '/var/opt/uwsapp'))

def DBNAME() -> str:
	return _getenv('UWSAPP_DBNAME',  '%s.db' % APPNAME)

_url_base = _getenv('UWSAPP_URL', '')

def URL(path: str = '') -> str:
	if _url_base == '':
		return path
	return urljoin(_url_base, path)
