# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsweb.views_test import WebViewTestCase

from http import HTTPStatus

class WebMiddlewareTest(WebViewTestCase):

	def test_auth(t):
		resp = t.client.get('/not.found')
		t.assertEqual(resp.status_code, HTTPStatus.FOUND)
		t.assertEqual(resp.headers['location'], '/auth/login?next=/not.found')

	def test_auth_login(t):
		with t.uwsweb_user():
			resp = t.client.get('/api')
			t.assertEqual(resp.status_code, HTTPStatus.OK)

	def test_auth_skip_login(t):
		resp = t.client.get('/auth/login')
		t.assertEqual(resp.status_code, HTTPStatus.OK)

	def test_auth_skip_static(t):
		resp = t.client.get('/static/not.found')
		t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)

	def test_auth_skip_admin(t):
		resp = t.client.get('/admin/login/')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
