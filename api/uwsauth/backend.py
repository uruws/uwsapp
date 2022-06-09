# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth.backends import BaseBackend

from hashlib import pbkdf2_hmac
from pathlib import Path
from uuid    import NAMESPACE_DNS
from uuid    import uuid5

from uwsapp import log

__salt = b'K0mP2LvwSIPnCI_hyqmEaeRN4_hHiQ1PC_ohAf1J6Eh3FAhD'

def _user_uuid(username: str) -> str:
	return str(uuid5(NAMESPACE_DNS, username))

def _user_password(pw: str) -> str:
	return pbkdf2_hmac('sha256', pw.encode(), __salt, 100000).hex()

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
				try:
					if b.__check_password(pwfn, password):
						pass
					else:
						log.error('%s: invalid password' % username)
				except Exception as err:
					log.error('could not read password file:', err)
			else:
				log.error('%s: file not found or is a symlink' % pwfn)
		else:
			log.error('%s: file not found or is a symlink' % fn)
		return None

	def __check_password(b, fn: Path, password: str) -> bool:
		pw = fn.read_text().strip()
		log.debug('auth password:', pw)
		upw = _user_password(password)
		log.debug('user password:', upw)
		if pw == upw:
			return True
		return False

	def get_user(b, user_id: str):
		log.debug('user_id:', user_id)
		user_id = user_id.strip()
		if user_id == '':
			return None
		return None
