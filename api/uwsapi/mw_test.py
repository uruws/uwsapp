# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsapi.views_test import ApiViewTestCase

from http import HTTPStatus

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
