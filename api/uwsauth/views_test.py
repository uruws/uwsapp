# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from http import HTTPStatus

class AuthViewsTests(TestCase):

	def test_login(t):
		resp = t.client.get('/auth/login')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		respdata = resp.json()
		t.assertEqual(len(respdata), 0)
