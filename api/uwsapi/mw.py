# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.conf import settings
from django.http import JsonResponse

from django.contrib.auth.models          import User
from django.contrib.sessions.backends.db import SessionStore

from http import HTTPStatus
from time import time

from uwsapp import config
from uwsapp import log

from uwsauth import backend

class ApiMiddleware:

	def __init__(mw, get_resp):
		mw.get_resp = get_resp

	def __auth(mw, req):
		# get session id
		try:
			sess_id = req.POST['session'].strip()
		except KeyError:
			sess_id = ''
		log.debug('session:', sess_id)
		if sess_id == '':
			return _unauth()
		# clear expired sessions
		req.session.clear_expired()
		log.debug('clear expired sessions')
		# check if exists
		log.debug('req.session:', req.session.session_key)
		if not req.session.exists(sess_id):
			log.debug('session not found:', sess_id)
			return _unauth()
		# load it
		sess = SessionStore(session_key = sess_id)
		if sess.is_empty():
			# reject empty sessions
			log.debug('empty session:', sess_id)
			log.debug('delete empty session:', sess_id)
			sess.delete()
			return _unauth()
		req.session = sess
		log.debug('req.session:', req.session.session_key)
		# check for corrupted session (if settings.SECRET changed or similar)
		try:
			last_seen = req.session['last_seen']
		except KeyError:
			log.debug('corrupted session:', sess_id)
			log.debug('delete corrupted session:', sess_id)
			req.session.delete()
			return _unauth()
		log.debug(sess_id, 'last seen:', last_seen)
		# set request user
		try:
			username = req.session['username']
		except KeyError:
			log.debug('invalid session:', sess_id, 'no username')
			log.debug('delete invalid session:', sess_id)
			req.session.delete()
			return _unauth()
		# load user from DB
		log.debug(sess_id, 'load username:', username)
		log.debug(sess_id, 'req.user:', req.user)
		try:
			u = User.objects.get(username = username)
		except User.DoesNotExist:
			log.error('invalid session:', sess_id, 'username not found:', username)
			log.debug('delete invalid session:', sess_id)
			req.session.delete()
			return _unauth()
		# check it is an actived user
		if not u.is_active:
			log.error('invalid session:', sess_id, 'inactive user:', u)
			log.debug('delete invalid session:', sess_id)
			req.session.delete()
			return _unauth()
		# check user still exists
		if backend.check_user(username) == '':
			log.error('invalid session:', sess_id, 'user does not exist anymore:', u)
			log.print('deactivate user:', u)
			u.is_active = False
			u.save()
			return _unauth()
		req.user = u
		log.debug(sess_id, 'req.user:', req.user)
		# save session
		log.debug('save session:', sess_id)
		req.session['last_seen'] = time()
		req.session.save()
		# process request
		return mw.get_resp(req)

	def __call__(mw, req):
		# ignore login url
		if req.path == settings.LOGIN_URL:
			resp = mw.get_resp(req)
		# ignore help urls
		elif req.path.startswith("/%s" % config.URL('help/')):
			resp = mw.get_resp(req)
		# ignore admin urls
		elif req.path.startswith("/%s" % config.URL('admin/')):
			resp = mw.get_resp(req)
		# auth the rest
		else:
			resp = mw.__auth(req)
		# post
		resp.headers['Server'] = 'uwsapi'
		return resp

def _unauth():
	resp = JsonResponse(dict())
	resp.status_code = HTTPStatus.UNAUTHORIZED
	return resp
