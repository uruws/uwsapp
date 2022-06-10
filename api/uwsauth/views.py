# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from datetime import datetime

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
			resp = JsonResponse({})
			resp.status_code = HTTPStatus.UNAUTHORIZED
			return resp
		else:
			sess = SessionStore()
			sess.create()
			sess['username'] = username
			sess['last_login'] = datetime.now()
			sess.save()
			return JsonResponse({'session': sess.session_key})
	resp = JsonResponse({})
	resp.status_code = HTTPStatus.BAD_REQUEST
	return resp
