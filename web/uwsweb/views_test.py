# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib  import contextmanager
from django.test import TestCase
from http        import HTTPStatus
from io          import StringIO

from django.contrib.auth.models import User
from unittest.mock              import MagicMock

from uwsapp import config
from uwsapp import log_test

from uwsweb import views

class WebViewTestCase(TestCase):

	def setUp(t):
		log_test.mock_setup()

	def tearDown(t):
		log_test.mock_teardown()

	def uwsweb_login(t):
		u = User(username = 'uwsweb', email = 'uwsweb@uwsapp.test')
		u.set_password('supersecret')
		u.save()
		t.assertTrue(t.client.login(username = 'uwsweb', password = 'supersecret'))

	def uwsweb_logout(t):
		t.client.logout()

	@contextmanager
	def uwsweb_user(t):
		try:
			t.uwsweb_login()
			yield
		finally:
			t.uwsweb_logout()

class MockMessages(object):
	__bup_messages = views.messages
	mock = None

	def setup(m):
		m.mock = MagicMock()
		views.messages = m.mock

	def teardown(m):
		views.messages = m.__bup_messages
		m.mock = None

@contextmanager
def mock_messages():
	try:
		m = MockMessages()
		m.setup()
		yield m
	finally:
		m.teardown()
		m = None

@contextmanager
def mock_api_client(v, req):
	bup = views.ApiClient
	try:
		cli = MagicMock()
		views.ApiClient = cli
		v.setup(req)
		yield
	finally:
		views.ApiClient = bup

class WebViewsTest(WebViewTestCase):

	def test_api_session(t):
		v = views.WebView()
		t.assertEqual(v.uwsapi_session(), 'NOUSER')

	def test_api_parse_response(t):
		v = views.WebView()
		resp = StringIO('{}')
		d = v.uwsapi_parse_response(resp)
		t.assertTrue(isinstance(d, dict))
		t.assertEqual(d, {})

	def test_api_parse_resp_error(t):
		v = views.WebView()
		resp = StringIO()
		with t.assertRaises(views.ApiError):
			v.uwsapi_parse_response(resp)

	def test_api_post(t):
		req = MagicMock()
		v = views.WebView()
		with mock_api_client(v, req):
			v.uwsapi_post('/ping', {})

	def test_base_msg(t):
		with mock_messages() as m:
			v = views.WebView()
			v.uwsweb_msg('testing')
			m.mock.success.assert_called_once_with(None, 'testing')

	def test_base_msg_error(t):
		with mock_messages() as m:
			v = views.WebView()
			v.uwsweb_msg_error('testing_error')
			m.mock.error.assert_called_once_with(None, 'testing_error')

	def test_cache_control(t):
		with t.uwsweb_user():
			resp = t.client.get('/')
			t.assertEqual(resp.status_code,              HTTPStatus.FOUND)
			t.assertEqual(resp.headers['content-type'],  'text/html; charset=utf-8')
			t.assertEqual(resp.headers['cache-control'],
				'max-age=5, must-revalidate, private, stale-if-error')

	def test_index_nologin(t):
		resp = t.client.get('/')
		t.assertEqual(resp.status_code,             HTTPStatus.FOUND)
		t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
		t.assertEqual(resp.headers['location'],     "/%s?next=/" % config.URL('auth/login'))

	def test_index_redirect(t):
		with t.uwsweb_user():
			resp = t.client.get('/')
			t.assertEqual(resp.status_code,             HTTPStatus.FOUND)
			t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
			t.assertEqual(resp.headers['location'],     '/logs/nq')

	def test_invalid_method(t):
		with t.uwsweb_user():
			resp = t.client.post('/', {})
			t.assertEqual(resp.status_code,             HTTPStatus.METHOD_NOT_ALLOWED)
			t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')

	def test_user(t):
		with t.uwsweb_user():
			resp = t.client.get('/user')
			t.assertEqual(resp.status_code,             HTTPStatus.OK)
			t.assertEqual(resp.headers['content-type'], 'text/html; charset=utf-8')
			t.assertEqual(resp.template_name[0],        'uwsweb/user.html')
			t.assertEqual(resp.context_data['title'],   'user')
