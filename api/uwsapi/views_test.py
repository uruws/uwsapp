# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from http import HTTPStatus

class ApiViewsTests(TestCase):

	def test_index(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		respdata = resp.json()
		t.assertEqual(respdata, dict())
