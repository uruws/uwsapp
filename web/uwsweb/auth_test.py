# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from unittest.mock import MagicMock

from contextlib  import contextmanager
from django.test import TestCase
from http        import HTTPStatus
from io          import StringIO

from uwsapp import user

from uwsweb import auth

class ApiClientMock(object):

	def POST(c, uri, data):
		u = user.load(data['username'])
		return StringIO(json.dumps(u))

class AuthViewTestCase(TestCase):

	@contextmanager
	def uwsapi_mock_client(t):
		bup = auth._newApiClient
		try:
			auth._newApiClient = MagicMock(return_value = ApiClientMock())
			yield
		finally:
			auth._newApiClient = bup

	def uwsapi_login(t):
		pass

	def uwsapi_logout(t):
		pass

	@contextmanager
	def uwsapi_user(t):
		try:
			t.uwsapi_login()
			yield
		finally:
			t.uwsapi_logout()

class AuthTests(AuthViewTestCase):

	def test_auth(t):
		with t.uwsapi_mock_client():
			t.assertFalse(t.client.login(username = 'uwsweb@uwsapp.test', password = 'supersecret'))
			resp = t.client.get('/not.found')
			t.assertEqual(resp.status_code, HTTPStatus.FOUND)
			t.assertEqual(resp.headers['location'], '/auth/login?next=/not.found')
