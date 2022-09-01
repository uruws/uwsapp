# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

class AppsIndexTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/apps/', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.json(), {})
