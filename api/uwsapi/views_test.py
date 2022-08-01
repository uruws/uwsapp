# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from http import HTTPStatus
from time import time

from django.contrib.auth.models          import User
from django.contrib.sessions.backends.db import SessionStore

class ApiMock(object):
	sess     = None
	sess_key = None
	username = 'uwstest@localhost'

	def mock_user(m):
		user = User(username = 'uwstest', email = m.username)
		user.save()
		return user

	def mock_login_setup(m, session_key = None):
		m.sess = SessionStore(session_key = session_key)
		m.sess.create()
		m.sess['last_seen'] = time()
		m.sess['username'] = m.username
		m.sess.save()
		m.sess_key = m.sess.session_key

	def mock_login_teardown(m, session_key = None):
		m.sess.delete()

class ApiViewsTests(TestCase):
	api = ApiMock()
	user = None

	def setUp(t):
		if t.user is None:
			t.user = t.api.mock_user()
		t.api.mock_login_setup()

	def tearDown(t):
		t.api.mock_login_teardown()

	def test_index_unauth(t):
		t.api.mock_login_teardown()
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		respdata = resp.json()
		t.assertEqual(respdata, dict())

	def test_error404(t):
		resp = t.client.post('/notfound', data = {'session': t.api.sess_key})
		t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
		respdata = resp.json()
		t.assertEqual(respdata, dict())
