# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from typing import Optional

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models   import User

from uwsapp import log

from uwsapp.api import ApiClient

def _get_resp_user(resp) -> dict[str, str]:
	log.debug('get_resp_user:', resp)
	u = {
		'uid': 'fake-uid',
		'name': 'fakename',
	}
	return u

def _check_credentials(username: str, password: str) -> Optional[User]:
	log.debug('username:', username)
	cli = ApiClient()
	try:
		resp = cli.POST('/auth/login', {
			'username': username,
			'password': password,
		})
	except Exception as err:
		log.error('api /auth/login:', err)
		return None
	u = _get_resp_user(resp)
	uid = u['uid']
	log.print('auth:', uid)
	try:
		user = User.objects.get(email = username)
	except User.DoesNotExist:
		log.debug(uid, 'create username:', username)
		user = User(username = u['name'], email = username)
		user.save()
	if not user.is_active:
		log.error('%s: inactive user' % uid, username)
		return None
	return user

class AuthBackend(BaseBackend):

	def authenticate(b, request, username: str = None, password: str = None) -> Optional[User]:
		log.debug('username:', username)
		if username is None or password is None:
			return None
		username = username.strip()
		password = password.strip()
		if username == '' or password == '':
			log.error('auth: empty username and/or password')
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
