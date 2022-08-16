# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

from uwsapi.views_test import ApiViewTestCase

from django.contrib.auth.models import User

from http import HTTPStatus

from uwsauth import mw

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

@contextmanager
def mock_check_user():
	bup = mw.backend
	try:
		mw.backend = MagicMock()
		mw.backend.check_user = MagicMock(return_value = '')
		yield
	finally:
		mw.backend = bup

class AuthMiddlewareTest(ApiViewTestCase):

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

	def test_session_last_seen(t):
		sess = t.uwsapi_session()
		sess.pop('last_seen')
		sess.save()
		resp = t.uwsapi_post('/ping', {})
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		t.assertDictEqual(resp.json(), {})

	def test_session_username(t):
		sess = t.uwsapi_session()
		sess.pop('username')
		sess.save()
		resp = t.uwsapi_post('/ping', {})
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		t.assertDictEqual(resp.json(), {})

	def test_check_user_error(t):
		with mock_check_user():
			resp = t.uwsapi_post('/ping', {})
			t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
			t.assertDictEqual(resp.json(), {})

	def test_check_user_not_active(t):
		u = User.objects.get(pk = 1)
		u.is_active = False
		u.save()
		resp = t.uwsapi_post('/ping', {})
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		t.assertDictEqual(resp.json(), {})

	def test_check_user_not_found(t):
		u = User.objects.get(pk = 1)
		u.delete()
		resp = t.uwsapi_post('/ping', {})
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		t.assertDictEqual(resp.json(), {})
