# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib  import contextmanager
from django.test import TestCase
from http        import HTTPStatus

from uwsapp import config

from django.contrib.auth.models import User

class WebViewTestCase(TestCase):

	def uwsweb_login(t):
		u = User(username = 'uwsweb', email = 'uwsweb@uwsapp.test')
		u.set_password('supersecret')
		u.save()
		t.assertTrue(t.client.login(username = 'uwsweb', password = 'supersecret'))

	def uwsweb_logout(t):
		t.client.logout()

	@contextmanager
	def uwsweb_user(t):
		try:
			t.uwsweb_login()
			yield
		finally:
			t.uwsweb_logout()

class WebViewsTests(WebViewTestCase):

	def test_index_nologin(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.FOUND)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.headers['location'], "/%s?next=/" % config.URL('auth/login'))

	def test_index_redirect(t):
		with t.uwsweb_user():
			resp = t.client.get('/')
			t.assertEqual(resp.status_code, HTTPStatus.FOUND)
			t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
			t.assertEqual(resp.headers['location'], '/logs/nq')

	def test_invalid_method(t):
		with t.uwsweb_user():
			resp = t.client.post('/', {})
			t.assertEqual(resp.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
			t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
