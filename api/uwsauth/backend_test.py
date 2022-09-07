# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

from http    import HTTPStatus
from pathlib import Path

from django.contrib.auth.models import User

from uwsapi.views_test import ApiViewTestCase

from uwsauth import backend

_authd = Path('/run/uwscli/auth')

@contextmanager
def mock_check_password(status = True, fail = False):
	def _chk(*args, **kwargs):
		if fail:
			raise Exception('mock_check_password_error')
		return status
	bup = backend._check_password
	try:
		backend._check_password = MagicMock(side_effect = _chk)
		yield
	finally:
		backend._check_password = bup

class AuthBackendTest(ApiViewTestCase):

	def test_login(t):
		t.assertTrue(t.client.login(username = 'uwsdev@uwsapp.local',
			password = 'supersecret'))

	def test_invalid_username(t):
		t.assertFalse(t.client.login(username = 'invalid@uwsapp.local',
			password = 'supersecret'))

	def test_invalid_password(t):
		t.assertFalse(t.client.login(username = 'uwsdev@uwsapp.local',
			password = 'invalid'))

	def test_auth_no_data(t):
		b = backend.AuthBackend()
		t.assertIsNone(b.authenticate(None))

	def test_auth_empty_data(t):
		b = backend.AuthBackend()
		t.assertIsNone(b.authenticate(None, username = '', password = ''))

	def test_get_user(t):
		b = backend.AuthBackend()
		t.assertIsNotNone(b.get_user(1))

	def test_get_user_not_found(t):
		b = backend.AuthBackend()
		t.assertIsNone(b.get_user(999))

	def test_get_user_inactive(t):
		u = User.objects.get(pk = 1)
		u.is_active = False
		u.save()
		b = backend.AuthBackend()
		t.assertIsNone(b.get_user(1))

	def test_check_user(t):
		uid = backend.check_user('uwstest@localhost')
		t.assertEqual(uid, 'dc7133eb-f64e-5d03-8d59-22d499224da6')

	def test_check_user_invalid(t):
		uid = backend.check_user('invalid@uwsapp.local')
		t.assertEqual(uid, '')

	def test_check_user_no_password(t):
		uid = backend.check_user('nopassword@localhost')
		t.assertEqual(uid, '')

	def test_check_credentials(t):
		with mock_check_password():
			uid = 'dc7133eb-f64e-5d03-8d59-22d499224da6'
			u = backend._check_credentials(uid, 'uwstest@localhost', '')
			t.assertEqual(u.username, 'uwstest')

	def test_check_credentials_invalid(t):
		uid = 'a9856e79-c3cd-55b6-89f6-762b8c2e388d'
		u = backend._check_credentials(uid, 'invalid@uwsapp.local', '')
		t.assertIsNone(u)

	def test_check_credentials_no_password(t):
		uid = '40ef0316-91d2-5654-99b2-fcf60b707d8f'
		u = backend._check_credentials(uid, 'nopassword@localhost', '')
		t.assertIsNone(u)

	def test_check_credentials_error(t):
		with mock_check_password(fail = True):
			uid = 'dc7133eb-f64e-5d03-8d59-22d499224da6'
			u = backend._check_credentials(uid, 'uwstest@localhost', '')
			t.assertIsNone(u)

	def test_load_user(t):
		uid = 'dc7133eb-f64e-5d03-8d59-22d499224da6'
		fn = _authd / uid / 'meta.json'
		u = backend._load_user(uid, fn, 'uwstest@localhost')
		t.assertIsNotNone(u)
		t.assertEqual(u.username, 'uwstest')

	def test_load_user_not_active(t):
		u = User.objects.get(pk = 1)
		u.is_active = False
		u.save()
		uid = 'dc7133eb-f64e-5d03-8d59-22d499224da6'
		fn = _authd / uid / 'meta.json'
		u = backend._load_user(uid, fn, 'uwstest@localhost')
		t.assertIsNone(u)

	def test_load_user_invalid(t):
		uid = 'a9856e79-c3cd-55b6-89f6-762b8c2e388d'
		fn = _authd / uid / 'meta-empty.json'
		u = backend._load_user(uid, fn, 'invalid@uwsapp.local')
		t.assertIsNone(u)

	def test_load_user_no_user(t):
		uid = 'a9856e79-c3cd-55b6-89f6-762b8c2e388d'
		fn = _authd / uid / 'meta-no-user.json'
		u = backend._load_user(uid, fn, 'invalid@uwsapp.local')
		t.assertIsNone(u)

	def test_load_user_username_error(t):
		uid = 'a9856e79-c3cd-55b6-89f6-762b8c2e388d'
		fn = _authd / uid / 'meta-username-error.json'
		u = backend._load_user(uid, fn, 'invalid@uwsapp.local')
		t.assertIsNone(u)
