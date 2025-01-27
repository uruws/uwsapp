# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsweb.auth_test import AuthViewTestCase

class WebLogsViewsTest(AuthViewTestCase):

	def test_nq_index(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/logs/nq')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.template_name[0], 'uwslogs/nq.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'], 'jobs')
		t.assertDictEqual(resp.context_data['nqlog'], {})

	def test_nq_tail(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/logs/nq/1823af52426.17746/tail')
		t.assertEqual(resp.status_code,             HTTPStatus.OK)
		t.assertEqual(resp.template_name[0],        'uwslogs/nq-tail.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'],   'job 1823af52426.17746')
		t.assertDictEqual(resp.context_data['job'], {})

	def test_appctl_index(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/logs/app-ctl')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.template_name[0], 'uwslogs/index.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'], 'app-ctl')
		t.assertDictEqual(resp.context_data['syslog'], {})

	def test_uwsq_index(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/logs/uwsq')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.template_name[0], 'uwslogs/index.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'], 'uwsq')
		t.assertDictEqual(resp.context_data['syslog'], {})
