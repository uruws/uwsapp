# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

class AuthViewsTests(TestCase):

	def test_index(t):
		resp = t.client.get('/auth/')
		t.assertEqual(resp.status_code, 200)
		respdata = resp.json()
		t.assertEqual(respdata['testing'], 'test0')
