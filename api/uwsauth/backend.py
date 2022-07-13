# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from typing import Optional

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models   import User

from pathlib import Path

from uwsapp import log
from uwsapp import user

def _user_uuid(username: str) -> str:
	return user.uuid(username)

def _user_password(pw: str) -> str:
	return user.password_hash(pw)

def _check_password(uid: str, fn: Path, password: str) -> bool:
	pw = fn.read_text().strip()
	upw = _user_password(password)
	if pw == upw:
		return True
	log.debug(uid, 'auth password:', pw)
	log.debug(uid, 'user password:', upw)
	return False

def _load_user(uid: str, fn: Path, username: str) -> Optional[User]:
	u = None
	with open(fn, 'r') as fh:
		u = json.load(fh)
	try:
		if u['name'] == '':
			log.error('%s: auth info no user name' % uid)
			return None
		if u['username'] != username:
			log.error('%s: auth info mismatch' % uid)
			return None
	except KeyError as err:
		log.error('%s: invalid auth info:' % uid, err)
		return None
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

def _check_credentials(uid: str, username: str, password: str) -> Optional[User]:
	fn = Path('/run/uwscli/auth/%s/meta.json' % uid)
	pwfn = Path('/run/uwscli/auth/%s/password' % uid)
	if fn.is_file() and not fn.is_symlink():
		if pwfn.is_file() and not pwfn.is_symlink():
			try:
				if _check_password(uid, pwfn, password):
					return _load_user(uid, fn, username)
				else:
					log.error('%s: invalid password' % uid)
			except Exception as err:
				log.error('check user credentials:', err)
		else:
			log.error('%s: file not found or is a symlink' % pwfn)
	else:
		log.error('%s: file not found or is a symlink' % fn)
	return None

def check_user(username: str) -> str:
	uid = _user_uuid(username)
	fn = Path('/run/uwscli/auth/%s/meta.json' % uid)
	pwfn = Path('/run/uwscli/auth/%s/password' % uid)
	if fn.is_file() and not fn.is_symlink():
		if pwfn.is_file() and not pwfn.is_symlink():
			if _load_user(uid, fn, username) is not None:
				return uid
		else:
			log.error('%s: file not found or is a symlink' % pwfn)
	else:
		log.error('%s: file not found or is a symlink' % fn)
	return ''

class AuthBackend(BaseBackend):

	def authenticate(b, request, username: str = None, password: str = None) -> Optional[User]:
		log.debug('username:', username)
		if username is None or password is None:
			return None
		username = username.strip()
		password = password.strip()
		if username == '' or password == '':
			return None
		uid = _user_uuid(username)
		log.debug('uid:', uid)
		return _check_credentials(uid, username, password)

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
