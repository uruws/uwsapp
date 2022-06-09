# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth.backends import BaseBackend

from uuid import NAMESPACE_DNS
from uuid import uuid5

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
		return None

	def get_user(b, user_id: str):
		log.debug('user_id:', user_id)
		user_id = user_id.strip()
		if user_id == '':
			return None
		return None
