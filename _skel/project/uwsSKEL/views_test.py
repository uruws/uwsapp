# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase
from http        import HTTPStatus

class SkelViewsTests(TestCase):

	def test_index(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.template_name[0], 'uwsSKEL/index.html')
		t.assertEqual(resp.context_data['title'], 'index')
