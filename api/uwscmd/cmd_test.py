# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from http import HTTPStatus

class ApiCmdTests(TestCase):

	def test_view(t):
		resp = t.client.get('/exec/testing')
		t.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
		respdata = resp.json()
		t.assertEqual(respdata, dict())
