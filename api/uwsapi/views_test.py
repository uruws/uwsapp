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
from uwsapp import log_test

class ApiMock(object):
	sess     = None
	sess_key = None
	username = 'uwsdev@uwsapp.local'
	user     = None

	def mock_user(m):
		user = User(username = 'uwsdev', email = m.username)
		user.set_password('supersecret')
		user.save()
		return user

	def mock_login_setup(m):
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

class ApiViewTestCase(TestCase):
	__api = ApiMock()

	def setUp(t):
		log_test.mock_setup()
		t.__api.mock_login_setup()

	def tearDown(t):
		t.__api.mock_login_teardown()
		log_test.mock_teardown()

	def uwsapi_post(t, uri, data):
		data['session'] = t.__api.sess_key
		return t.client.post(uri, data = data)

	def uwsapi_session(t):
		return t.__api.sess

class ApiViewTest(ApiViewTestCase):

	def test_index_unauth(t):
		t.tearDown()
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		respdata = resp.json()
		t.assertEqual(respdata, dict())

	def test_error404(t):
		resp = t.uwsapi_post('/notfound', {})
		t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
		respdata = resp.json()
		t.assertEqual(respdata, dict())

class IndexTest(ApiViewTestCase):

	def test_get(t):
		if not config.DEBUG():
			resp = t.uwsapi_post('/', {})
			t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
			respdata = resp.json()
			t.assertEqual(respdata, dict())

	def test_debug(t):
		bup = config.DEBUG
		try:
			config.DEBUG = MagicMock(return_value = True)
			resp = t.uwsapi_post('/', {})
			t.assertEqual(resp.status_code, HTTPStatus.OK)
			respdata = resp.json()
			t.assertEqual(len(respdata), 2)
		finally:
			config.DEBUG = bup
