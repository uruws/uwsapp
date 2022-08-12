# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

class AuthViewTest(ApiViewTestCase):

	def test_login(t):
		resp = t.client.post('/auth/login', {
			'username': 'uwstest@localhost', 'password': 'supersecret',
		})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.json()['name'], 'uwstest')

	def test_login_unauth(t):
		resp = t.client.post('/auth/login', {})
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)

	def test_login_bad_request(t):
		resp = t.client.get('/auth/login')
		t.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
		t.assertDictEqual(resp.json(), {})
