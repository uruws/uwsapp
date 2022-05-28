# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

class ApiViewsTests(TestCase):

	def test_index(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, 200)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertListEqual(sorted([str(t.name) for t in resp.templates]),
			['uwsweb/base.html', 'uwsweb/index.html'])
