# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

class CmdViewsTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/exec/', {'command': 'testing', 'app': 'apptest'})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.json(), {
			'command': '/opt/uwsapp/api/libexec/apicmd.sh uwsdev testing apptest',
			'output': '',
		})

	def test_index_missing_args(t):
		resp = t.uwsapi_post('/exec/', {})
		t.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
		t.assertEqual(resp.json(), {})
