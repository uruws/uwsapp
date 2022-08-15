# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from unittest.mock import MagicMock

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

from uwslogs import syslog

class SyslogTest(ApiViewTestCase):

	def test_uwsq(t):
		resp = t.uwsapi_post('/logs/uwsq', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		data = resp.json()
		t.assertListEqual(list(data.keys()), [str(i) for i in range(13)])
		t.assertDictEqual(data['0'], {
			'error': False,
			'message': 'Buildpack/build.py --src app/src --target app --version 2.75.0',
			'source': 'uwsq',
			'timestamp': 'Fri, 15 Jul 2022 16:45:03 +0000',
			'user': 'uwscli',
			'warning': False,
		})

	def test_uwsq_empty_line(t):
		t.assertIsNone(syslog._uwsq(''))

	def test_uwsq_file_not_found(t):
		d = syslog.uwsq(filename = 'not.found')
		t.assertEqual(len(d), 0)

	def test_appctl(t):
		resp = t.uwsapi_post('/logs/app-ctl', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		data = resp.json()
		t.assertListEqual(list(data.keys()), [str(i) for i in range(111)])
		t.assertDictEqual(data['0'], {
			'error': False,
			'message': 'apptest-east meteor/worker deploy 2.75.0-bp35',
			'source': 'app-ctl',
			'timestamp': 'Fri, 15 Jul 2022 17:17:54 +0000',
			'user': 'uws',
			'warning': False,
		})

	def test_appctl_empty_line(t):
		t.assertIsNone(syslog._app_ctl(''))

	def test_appctl_file_not_found(t):
		d = syslog.app_ctl(filename = 'not.found')
		t.assertEqual(len(d), 0)
