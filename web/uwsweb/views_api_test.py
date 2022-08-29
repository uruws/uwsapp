# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsweb.auth_test import AuthViewTestCase

from uwsweb import views_api

class WebApiViewsTest(AuthViewTestCase):

	def test_get(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/api')
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.template_name[0], 'uwsweb/api.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'], 'api')
		t.assertEqual(resp.context_data['title_desc'], 'API Client')
		t.assertEqual(resp.context_data['template_name'], resp.template_name[0])
		t.assertEqual(resp.context_data['api_endpoint'], '/api/ping')
		t.assertEqual(resp.context_data['api_params'], '{"session": "XXXXXXX"}')
		t.assertDictEqual(resp.context_data['api_response'], {})

	def test_post_empty(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.post('/api', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.template_name[0], 'uwsweb/api.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['api_endpoint'], '/api/ping')
		t.assertDictEqual(resp.context_data['api_response'], {})

	def test_post_params_error(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.post('/api', {'api_params': ''})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.template_name[0], 'uwsweb/api.html')
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['api_endpoint'], '/api/ping')
		t.assertDictEqual(resp.context_data['api_response'], {})

	def test_resp_status_code(t):
		t.assertEqual(views_api._resp_status(200), '200 OK')
		t.assertEqual(views_api._resp_status(400), '400 BAD REQUEST')
		t.assertEqual(views_api._resp_status(499), '499 INVALID STATUS')
