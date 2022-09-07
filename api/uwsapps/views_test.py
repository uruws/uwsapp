# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http          import HTTPStatus
from unittest.mock import MagicMock

from uwsapp import user

from uwsapi.views_test import ApiViewTestCase

from . import views

class AppsViewsTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/apps/', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.maxDiff = None
		t.assertListEqual(sorted(resp.json().keys()), [
			'build',
			'build_command',
			'commands',
			'deploy',
			'uid',
		])

	def test_index_user_error(t):
		def _user_error(*args, **kwargs):
			raise user.Error('testing')
		bup = views.user.apps
		try:
			views.user.apps = MagicMock(side_effect = _user_error)
			resp = t.uwsapi_post('/apps/', {})
			t.assertEqual(resp.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			views.user.apps = bup

	def test_app_info(t):
		resp = t.uwsapi_post('/apps/app-test/info', {})
		# ~ t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.maxDiff = None
		t.assertDictEqual(resp.json(), {
			'cluster': 'ktest',
			'desc': 'App test',
			'name': 'app-test',
			'pod': 'pod/test',
		})

	# ~ def test_index_user_error(t):
		# ~ def _user_error(*args, **kwargs):
			# ~ raise user.Error('testing')
		# ~ bup = views.user.apps
		# ~ try:
			# ~ views.user.apps = MagicMock(side_effect = _user_error)
			# ~ resp = t.uwsapi_post('/apps/', {})
			# ~ t.assertEqual(resp.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
		# ~ finally:
			# ~ views.user.apps = bup
