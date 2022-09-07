#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

from os import environ
environ['UWSAPP_AUTH_SECRET'] = 'supersecret'

from uwsapp import config
from uwsapp import user

class UserTest(unittest.TestCase):

	def test_defaults(t):
		t.assertNotEqual(config.AUTH_SECRET_KEY(), '')

	def test_uuid(t):
		t.assertEqual(user.uuid('testing'),
			'013fad7b-475f-55b4-b2b7-0da6c41293a8')

	def test_password_hash(t):
		t.assertEqual(user.password_hash('testing'),
			'cb852aa8da335ac892f88adf4f8401f6f24f7640879163a41dca9f6ccdf54c70')

	def test_user_load(t):
		u = user.load('uwstest@localhost')
		t.assertDictEqual(u, {
			'is_admin':    True,
			'is_operator': True,
			'name':        'uwstest',
			'uid':         'dc7133eb-f64e-5d03-8d59-22d499224da6',
			'username':    'uwstest@localhost',
		})

	def test_user_apps(t):
		apps = user.apps('uwstest@localhost')
		t.maxDiff = None
		t.assertDictEqual(apps, {
			'build': {
				'app': {
					'desc': 'App',
					'cluster': 'None',
					'pod': 'None',
				},
			},
			'build_command': 'app-build',
			'commands': [
				'app-deploy',
				'app-events',
				'app-logs',
				'app-restart',
				'app-rollin',
				'app-scale',
				'app-status',
				'app-top',
			],
			'deploy': {
				'app-test': {
					'desc': 'App test',
					'cluster': 'ktest',
					'pod': 'pod/test',
				},
			},
			'uid': 'dc7133eb-f64e-5d03-8d59-22d499224da6',
		})

	def test_user_apps_json_error(t):
		bup = user.json.load
		def _json_error(*args, **kwargs):
			raise Exception('testing')
		try:
			user.json.load = MagicMock(side_effect = _json_error)
			with t.assertRaises(user.Error):
				user.apps('uwstest@localhost')
		finally:
			user.json.load = bup

if __name__ == '__main__':
	unittest.main()
