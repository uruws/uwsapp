# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

class AuthBackendTest(ApiViewTestCase):

	def test_login(t):
		t.assertTrue(t.client.login(username = 'uwsdev@uwsapp.local', password = 'supersecret'))
