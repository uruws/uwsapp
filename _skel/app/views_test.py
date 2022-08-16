# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

class SkelIndexTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/SKEL', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.json(), {})
