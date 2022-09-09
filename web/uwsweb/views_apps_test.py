# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsweb.auth_test import AuthViewTestCase

from uwsweb import views_api

class WebAppsViewsTest(AuthViewTestCase):

	#
	# Apps
	#

	def test_apps(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/apps')
		t.assertEqual(resp.status_code,              HTTPStatus.OK)
		t.assertEqual(resp.template_name[0],         'uwsapps/index.html')
		t.assertEqual(resp.headers['content-type'],  'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'],    'apps')
		t.assertDictEqual(resp.context_data['apps'], {})

	#
	# Apps Build
	#

	def test_apps_build(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/apps/build')
		t.assertEqual(resp.status_code,              HTTPStatus.OK)
		t.assertEqual(resp.template_name[0],         'uwsapps/build-index.html')
		t.assertEqual(resp.headers['content-type'],  'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'],    'apps build')
		t.assertDictEqual(resp.context_data['apps'], {})

	#
	# App Build
	#

	def test_app_build(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/app/testing/build')
		t.assertEqual(resp.status_code,                HTTPStatus.OK)
		t.assertEqual(resp.template_name[0],           'uwsapps/build.html')
		t.assertEqual(resp.headers['content-type'],    'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'],      'app build: testing')
		t.assertEqual(resp.context_data['title_desc'], 'App Build: testing')

	#
	# App Control
	#

	def test_app_control(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/app/testing/status')
		t.assertEqual(resp.status_code,                HTTPStatus.OK)
		t.assertEqual(resp.template_name[0],           'uwsapps/control.html')
		t.assertEqual(resp.headers['content-type'],    'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'],      'app-status testing')
		t.assertEqual(resp.context_data['title_desc'], 'App Status: testing')

	#
	# App Home
	#

	def test_app_home(t):
		resp = None
		with t.uwsapi_user():
			resp = t.client.get('/app/testing')
		t.assertEqual(resp.status_code,                HTTPStatus.OK)
		t.assertEqual(resp.template_name[0],           'uwsapps/home.html')
		t.assertEqual(resp.headers['content-type'],    'text/html; charset=utf-8')
		t.assertEqual(resp.context_data['title'],      'app: testing')
		t.assertEqual(resp.context_data['title_desc'], 'App: testing')
