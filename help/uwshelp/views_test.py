# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase
from http        import HTTPStatus

from uwsapp import config
from uwsapp import log_test

class HelpViewsTests(TestCase):

	def setUp(t):
		log_test.mock_setup()

	def tearDown(t):
		log_test.mock_teardown()

	def test_cache_control(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.headers['content-type'],  'text/html; charset=utf-8')
		t.assertEqual(resp.headers['cache-control'],
			'max-age=5, must-revalidate, private, stale-if-error')

	def test_index(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.template_name[0], 'uwshelp/index.html')
		t.assertEqual(resp.context_data['title'], 'index')
		t.assertTrue(len(resp.context_data['api_docs']) > 0)
		t.assertTrue(len(resp.context_data['web_docs']) > 0)

	def test_help(t):
		resp = t.client.get('/web/api')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.template_name[0], 'uwshelp/doc.html')
		t.assertEqual(resp.context_data['title'], '/web/api')
		t.assertTrue(len(resp.context_data['doc']) > 0)

	def test_help_error(t):
		resp = t.client.get('/notfound')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.template_name[0], 'uwshelp/doc.html')
		t.assertEqual(resp.context_data['title'], '/notfound')
		t.assertEqual(resp.context_data['doc'],
			"""<pre class="w3-container w3-red">ERROR: [Errno 2] No such file or directory: '/opt/uwsapp/help/docs/notfound.md'</pre>""")
