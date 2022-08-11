# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from unittest.mock import MagicMock

from contextlib import contextmanager
from http       import HTTPStatus
from io         import StringIO

from django.test                import TestCase
from django.contrib.auth.models import User

from uwsapp import log_test
from uwsapp import user

from uwsweb import auth

class ApiClientMock(object):

	def POST(c, uri, data):
		u = user.load(data['username'])
		return StringIO(json.dumps(u))

class AuthViewTestCase(TestCase):

	def setUp(t):
		log_test.mock_setup()

	def tearDown(t):
		t.uwslog = None
		log_test.mock_teardown()

	@contextmanager
	def uwsapi_mock_client(t):
		bup = auth._newApiClient
		try:
			auth._newApiClient = MagicMock(return_value = ApiClientMock())
			yield
		finally:
			auth._newApiClient = bup

	def uwsapi_login(t):
		with t.uwsapi_mock_client():
			t.assertTrue(t.client.login(username = 'uwsdev@uwsapp.local', password = 'supersecret'))

	def uwsapi_logout(t):
		t.client.logout()

	@contextmanager
	def uwsapi_user(t):
		try:
			t.uwsapi_login()
			yield
		finally:
			t.uwsapi_logout()

class AuthTests(AuthViewTestCase):

	def test_auth_fail(t):
		with t.uwsapi_mock_client():
			t.assertFalse(t.client.login(username = 'uwsweb@uwsapp.test', password = 'supersecret'))
			resp = t.client.get('/not.found')
			t.assertEqual(resp.status_code, HTTPStatus.FOUND)
			t.assertEqual(resp.headers['location'], '/auth/login?next=/not.found')

	def test_auth(t):
		with t.uwsapi_user():
			resp = t.client.get('/not.found')
			t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)

	def test_auth_inactive_user(t):
		with t.uwsapi_user():
			u = User.objects.get(email = 'uwsdev@uwsapp.local')
			u.is_active = False
			u.save()
			with t.uwsapi_mock_client():
				t.assertIsNone(auth._check_credentials(None, 'uwsdev@uwsapp.local', 'supersecret'))
