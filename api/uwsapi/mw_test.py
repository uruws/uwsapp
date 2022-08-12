# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

from uwsapi.views_test import ApiViewTestCase

from http import HTTPStatus

from uwsapi import mw

@contextmanager
def mock_session(is_empty = False):
	bup = mw.SessionStore
	try:
		sess = MagicMock()
		sess.is_empty = MagicMock(return_value = is_empty)
		mw.SessionStore = MagicMock(return_value = sess)
		yield
	finally:
		mw.SessionStore = bup

class ApiMiddlewareTest(ApiViewTestCase):

	def test_unauth(t):
		resp = t.client.get('/not.found')
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		t.assertDictEqual(resp.json(), {})

	def test_auth(t):
		resp = t.uwsapi_post('/not.found', {})
		t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
		t.assertDictEqual(resp.json(), {})

	def test_auth_ignore_login(t):
		resp = t.client.post('/auth/login', {
			'username': 'uwstest@localhost', 'password': 'supersecret',
		})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.json()['name'], 'uwstest')

	def test_auth_ignore_admin(t):
		resp = t.client.get('/admin/')
		t.assertEqual(resp.status_code, HTTPStatus.FOUND)

	def test_session_not_found(t):
		resp = t.client.post('/', {'session': 'abcdef123456'})
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)

	def test_session_empty(t):
		with mock_session(is_empty = True):
			resp = t.uwsapi_post('/ping', {})
			t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
