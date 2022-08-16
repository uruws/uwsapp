# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsapi.views_test import ApiViewTestCase

class CmdIndexTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/cmd', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertEqual(resp.json(), {})
