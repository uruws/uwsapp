# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth.backends import BaseBackend

from pathlib import Path
from uuid    import NAMESPACE_DNS
from uuid    import uuid5

from uwsapp import log

def _user_uuid(username: str) -> str:
	return str(uuid5(NAMESPACE_DNS, username))

class AuthBackend(BaseBackend):

	def authenticate(b, request, username: str = None, password: str = None):
		log.debug('username:', username)
		if username is None or password is None:
			return None
		username = username.strip()
		password = password.strip()
		if username == '' or password == '':
			return None
		uid = _user_uuid(username)
		log.debug('uid:', uid)
		return b.__load_user(uid, username, password)

	def __load_user(b, uid: str, username: str, password: str):
		fn = Path('/run/uwscli/auth/%s/meta.json' % uid)
		pwfn = Path('/run/uwscli/auth/%s/password' % uid)
		if fn.is_file() and not fn.is_symlink():
			if pwfn.is_file() and not pwfn.is_symlink():
				pass
			else:
				log.error('%s: file not found or is a symlink' % pwfn)
		else:
			log.error('%s: file not found or is a symlink' % fn)
		return None

	def get_user(b, user_id: str):
		log.debug('user_id:', user_id)
		user_id = user_id.strip()
		if user_id == '':
			return None
		return None
