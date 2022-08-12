# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from django.contrib.auth.models import User

from uwsapi.views_test import ApiViewTestCase

from uwsauth import backend

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
