# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http          import HTTPStatus
from unittest.mock import MagicMock

from uwsweb.auth_test import AuthViewTestCase

from uwsweb import views_apps

def mock_apicmd_view(resp = {}, fail = False):
	def _fail(*args, **kwargs):
		raise views_apps.ApiError('mock_api_error')
	v = MagicMock()
	v._resp = MagicMock()
	if fail:
		v.uwsapi_post = MagicMock(side_effect = _fail)
	else:
		v.uwsapi_post = MagicMock(return_value = v._resp)
	v.uwsapi_parse_response = MagicMock(return_value = resp)
	v.uwsweb_msg_error = MagicMock()
	return v

class WebAppsViewsTest(AuthViewTestCase):

	#
	# utils
	#

	def test_apicmd(t):
		d = {}
		v = mock_apicmd_view({'output': 'testing'})
		views_apps._apicmd(v, d, 'status', 'testing')
		t.assertDictEqual(d, {
			'app_action':                'status',
			'app_action_response':       {'output': 'testing'},
			'app_action_response_lines': 3,
		})

	def test_apicmd_output_error(t):
		d = {}
		v = mock_apicmd_view()
		views_apps._apicmd(v, d, 'status', 'testing')
		t.assertDictEqual(d, {
			'app_action':                'status',
			'app_action_response':       {},
			'app_action_response_lines': 0,
		})

	def test_apicmd_api_error(t):
		d = {}
		v = mock_apicmd_view({'output': 'testing'}, fail = True)
		views_apps._apicmd(v, d, 'status', 'testing')
		t.assertDictEqual(d, {
			'app_action':                'status',
			'app_action_response':       {},
			'app_action_response_lines': 0,
		})

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
		t.assertEqual(resp.context_data['title'],      'app-build testing')
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
		t.assertEqual(resp.context_data['title'],      'testing')
		t.assertEqual(resp.context_data['title_desc'], 'App: testing')
