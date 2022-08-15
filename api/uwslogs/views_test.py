# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

class LogsViewsTest(ApiViewTestCase):

	def test_index(t):
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
