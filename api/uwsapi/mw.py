# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.conf import settings
from django.http import JsonResponse

from django.contrib.sessions.backends.db import SessionStore

from http import HTTPStatus

from uwsapp import log

class ApiMiddleware:

	def __init__(mw, get_resp):
		mw.get_resp = get_resp

	def __auth(mw, req):
		try:
			sess_id = req.POST['session'].strip()
		except KeyError:
			sess_id = ''
		log.debug('session:', sess_id)
		if sess_id == '':
			return _unauth()
		log.debug('req.session:', req.session.session_key)
		log.debug('clear expired sessions')
		req.session.clear_expired()
		if not req.session.exists(sess_id):
			log.debug('session not found:', sess_id)
			return _unauth()
		sess = SessionStore(session_key = sess_id)
		if sess.is_empty():
			log.debug('empty session:', sess_id)
			log.debug('delete empty session:', sess_id)
			sess.delete()
			return _unauth()
		req.session = sess
		log.debug('req.session:', req.session.session_key)
		return mw.get_resp(req)

	def __call__(mw, req):
		if req.path == settings.LOGIN_URL:
			resp = mw.get_resp(req)
		elif req.path.startswith('/admin/'):
			resp = mw.get_resp(req)
		else:
			resp = mw.__auth(req)
		resp.headers['Server'] = 'uwsapi'
		return resp

def _unauth():
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.UNAUTHORIZED
	return resp
