# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsweb.views_test import WebViewTestCase

from django.test import TestCase
from http        import HTTPStatus

from uwsapp import config

class HelpViewsTests(WebViewTestCase):

	def test_auth(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.FOUND)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.headers['location'], '/auth/login?next=/')

	def test_auth_login(t):
		with t.uwsweb_user() as u:
			resp = t.client.get('/api')
			t.assertEqual(resp.status_code, HTTPStatus.FOUND)
			t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
			t.assertEqual(resp.headers['location'], '/auth/login?next=/api')
