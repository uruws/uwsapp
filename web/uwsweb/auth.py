# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models   import User

from uwsapp import log

def _check_credentials(username: str, password: str) -> Optional[User]:
	log.debug('username:', username)
	return User(username = username)

class AuthBackend(BaseBackend):

	def authenticate(b, request, username: str = None, password: str = None):
		log.debug('username:', username)
		if username is None or password is None:
			return None
		username = username.strip()
		password = password.strip()
		if username == '' or password == '':
			return None
		return _check_credentials(uid, username, password)

	def get_user(b, user_id):
		log.debug('user_id:', user_id)
		try:
			return User.objects.get(pk = user_id)
		except User.DoesNotExist:
			return None
