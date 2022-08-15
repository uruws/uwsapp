# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

from uwslogs import views

class LogsViewsTest(ApiViewTestCase):

	def test_index_uwsq(t):
		resp = t.uwsapi_post('/logs/uwsq', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertIsInstance(resp.json(), dict)

	def test_index_appctl(t):
		resp = t.uwsapi_post('/logs/app-ctl', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertIsInstance(resp.json(), dict)

	def test_index_bad_request(t):
		resp = t.uwsapi_post('/logs/invalid', {})
		t.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
		t.assertDictEqual(resp.json(), {})

	def test_index_error(t):
		def _err(*args, **kwargs):
			raise Exception('mock_index_error')
		bup = views.syslog
		try:
			# mock
			views.syslog = MagicMock()
			views.syslog.app_ctl = MagicMock(side_effect = _err)
			# test
			resp = t.uwsapi_post('/logs/uwsq', {})
			t.assertEqual(resp.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
			t.assertDictEqual(resp.json(), {})
		finally:
			views.syslog = bup

	def test_nq_index(t):
		resp = t.uwsapi_post('/logs/nq/index', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertIsInstance(resp.json(), dict)
