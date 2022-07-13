# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models   import User

from uwsapp import log

from uwsapp.api import ApiClient

def _check_credentials(username: str, password: str) -> Optional[User]:
	log.debug('username:', username)
	cli = ApiClient()
	cli.POST('/auth/login', {
		'username': username,
		'password': password,
	})
	return None

class AuthBackend(BaseBackend):

	def authenticate(b, request, username: str = None, password: str = None) -> Optional[User]:
		log.debug('username:', username)
		if username is None or password is None:
			return None
		username = username.strip()
		password = password.strip()
		if username == '' or password == '':
			return None
		return _check_credentials(username, password)

	def get_user(b, user_id) -> Optional[User]:
		log.debug('user_id:', user_id)
		user = None
		try:
			user = User.objects.get(pk = user_id)
		except User.DoesNotExist:
			return None
		if not user.is_active:
			log.error('inactive user:', user)
			return None
		return user
