# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from http import HTTPStatus

class ApiMiddlewareTest(TestCase):

	def test_auth(t):
		resp = t.client.get('/not.found')
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		t.assertDictEqual(resp.json(), {})
