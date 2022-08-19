#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

from uwsapp import config

class Test(unittest.TestCase):

	def test_defaults(t):
		t.assertNotEqual(config.SECRET_KEY(), '')
		t.assertTrue(config.TESTING())
		t.assertListEqual(config.ALLOWED_HOSTS(), ['localhost'])
		t.assertEqual(config.DBDIR().as_posix(), '/var/opt/uwsapp')
		t.assertEqual(config.DBNAME(), 'app.db')
		t.assertEqual(config._url_base, '')

	def test_secrets(t):
		t.assertEqual(len(config.SECRET_KEY()), 64)
		t.assertEqual(config.AUTH_SECRET_KEY(), b'supersecret')
		t.assertEqual(len(config.AUTH_SECRET_KEY()), 11)

	def test_getenv_unset(t):
		t.assertEqual(config._getenv('UWSAPP_TESTING_UNSET', 'testing'), 'testing')

	def test_URLs(t):
		t.assertEqual(config.URL(''), '')
		t.assertEqual(config.URL('auth/testing/'), 'auth/testing/')
		try:
			config._url_base = 'testing/'
			t.assertEqual(config.URL('auth/'), 'testing/auth/')
			t.assertEqual(config.URL('auth'), 'testing/auth')
		finally:
			config._url_base = ''

	def test_api_defaults(t):
		t.assertEqual(config.API_HOST(),     'localhost')
		t.assertEqual(config.API_PORT(),     '443')
		t.assertEqual(config.API_TIMEOUT(),  '15')
		t.assertEqual(config.API_CERTFILE(), '')
		t.assertEqual(config.API_KEYFILE(),  '')
		t.assertEqual(config.API_KEYPASS(),  '')

	def test_cli_defaults(t):
		t.assertEqual(config.CLI_LOGSDIR().as_posix(), '/run/uwscli/logs')
		t.assertEqual(config.CLI_NQDIR().as_posix(),   '/run/uwscli/nq')
		t.assertEqual(config.CLI_SSHCMD().as_posix(),  '/usr/bin/ssh')

if __name__ == '__main__':
	unittest.main()
