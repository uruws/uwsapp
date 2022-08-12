# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.contrib.auth        import authenticate
from django.contrib.auth.models import User
from django.http                import JsonResponse

from django.contrib.sessions.backends.db import SessionStore

from http    import HTTPStatus
from time    import time

from uwsapp import log
from uwsapp import user as libuser

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
			u = libuser.load(username)
			sess = SessionStore()
			sess.create()
			sess['username'] = username
			sess['last_seen'] = time()
			sess.set_expiry(3600) # after one hour of inactivity
			sess.save()
			u['session'] = sess.session_key
			return JsonResponse(u)
	resp = JsonResponse({})
	resp.status_code = HTTPStatus.BAD_REQUEST
	return resp
