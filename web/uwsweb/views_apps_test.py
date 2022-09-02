# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsweb.auth_test import AuthViewTestCase

from uwsweb import views_api

class WebAppsViewsTest(AuthViewTestCase):

	def test_get(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/apps')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.template_name[0], 'uwsapps/index.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'], 'apps')
		t.assertDictEqual(resp.context_data['apps'], {})
