# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth.backends import BaseBackend

from uwsapp import log

class AuthBackend(BaseBackend):

	def authenticate(b, request, username = None, password = None):
		log.debug('req:', request)
		log.debug('username:', username)
		log.debug('session:', request.session.session_key)
		return None

	def get_user(b, user_id):
		log.debug('user_id:', user_id)
		return None
