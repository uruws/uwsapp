# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from http          import HTTPStatus
from unittest.mock import MagicMock

from uwsapp import user

from uwsapi.views_test import ApiViewTestCase

from . import views

class AppsIndexTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/apps/', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.maxDiff = None
		t.assertEqual(resp.json(), {
			'build': {
				'app': 'App web and workers',
				'cs': 'Crowdsourcing',
				'infra-ui': 'Infra-UI',
				'nlpsvc': 'NLPService',
			},
			'build_command': 'app-build',
			'commands': ['app-events', 'app-logs', 'app-status', 'app-top'],
			'deploy': {
				'app-east': 'App web, east cluster',
				'app-west': 'App web, west cluster',
				'apptest-east': 'App web, test cluster (east)',
				'apptest-west': 'App web, test cluster (west)',
				'cs': 'Crowdsourcing',
				'cs-test': 'Crowdsourcing test',
				'infra-ui-prod': 'Infra-UI production',
				'infra-ui-test': 'Infra-UI testing',
				'nlp-category': 'NLPService - Category',
				'nlp-sentiment-twitter': 'NLPService - Sentiment Twitter',
				'worker': 'App worker',
				'worker-test': 'App worker test',
			},
			'uid': '7044e95f-e20e-54be-9ce1-efa08e2b5a11',
		})

	def test_user_error(t):
		def _user_error(*args, **kwargs):
			raise user.Error('testing')
		bup = views.user.apps
		try:
			views.user.apps = MagicMock(side_effect = _user_error)
			resp = t.uwsapi_post('/apps/', {})
			t.assertEqual(resp.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
		finally:
			views.user.apps = bup
