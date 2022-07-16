# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from uwsapp import config

class WebViewsTests(TestCase):

	def test_index_nologin(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, 302)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.headers['location'], "/%s?next=/" % config.URL('auth/login'))
