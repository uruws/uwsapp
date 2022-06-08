# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth import authenticate
from django.http         import JsonResponse

from django.contrib.sessions.backends.db import SessionStore

from http import HTTPStatus

def login(req):
	if req.method == 'POST':
		try:
			username = req.POST['username']
			password = req.POST['password']
		except KeyError:
			username = None
			password = None
		user = authenticate(req, username = username, password = password)
		if user is None:
			resp = JsonResponse(dict())
			resp.status_code = HTTPStatus.UNAUTHORIZED
			return resp
		else:
			sess = SessionStore()
			sess['username'] = username
			sess.create()
			resp = JsonResponse(dict(
				session = sess.session_key,
			))
			return resp
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.BAD_REQUEST
	return resp
