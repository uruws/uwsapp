# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from django.test import TestCase

from http import HTTPStatus
from io   import StringIO
from time import time

from django.contrib.auth.models          import User
from django.contrib.sessions.backends.db import SessionStore

from uwsapp import config
from uwsapp import log

_bup_outfh = log._outfh
_bup_errfh = log._errfh

class ApiMock(object):
	sess     = None
	sess_key = None
	username = 'uwstest@localhost'
	user     = None

	def mock_user(m):
		user = User(username = 'uwstest', email = m.username)
		user.save()
		return user

	def mock_login_setup(m):
		if not config.DEBUG():
			log._outfh = StringIO()
			log._errfh = StringIO()
		m.user = m.mock_user()
		m.sess = SessionStore()
		m.sess.create()
		m.sess['last_seen'] = time()
		m.sess['username'] = m.username
		m.sess.save()
		m.sess_key = m.sess.session_key

	def mock_login_teardown(m):
		m.sess.delete()
		if m.user.pk is not None:
			m.user.delete()
		if not config.DEBUG():
			log._outfh = _bup_outfh
			log._errfh = _bup_errfh

class ApiViewTests(TestCase):
	api = ApiMock()

	def setUp(t):
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

class IndexTests(TestCase):
	api = ApiMock()

	def setUp(t):
		t.api.mock_login_setup()

	def tearDown(t):
		t.api.mock_login_teardown()

	def test_get(t):
		resp = t.client.post('/', data = {'session': t.api.sess_key})
		t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
		respdata = resp.json()
		t.assertEqual(respdata, dict())

	def test_debug(t):
		bup = config.DEBUG
		try:
			config.DEBUG = MagicMock(return_value = True)
			resp = t.client.post('/', data = {'session': t.api.sess_key})
			t.assertEqual(resp.status_code, HTTPStatus.OK)
			respdata = resp.json()
			t.assertEqual(len(respdata), 2)
		finally:
			config.DEBUG = bup
