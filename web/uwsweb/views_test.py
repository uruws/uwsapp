# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib  import contextmanager
from django.test import TestCase

from uwsapp import config

class WebViewTestCase(TestCase):

	def uwsweb_login(t):
		t.client.login()

	def uwsweb_logout(t):
		t.client.logout()

	@contextmanager
	def uwsweb_user(t):
		try:
			t.assertTrue(t.uwsweb_login())
			yield
		finally:
			t.assertTrue(t.uwsweb_logout())

class WebViewsTests(WebViewTestCase):

	def test_index_nologin(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, 302)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.headers['location'], "/%s?next=/" % config.URL('auth/login'))
