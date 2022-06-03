#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

from uwsapp import config

class Test(unittest.TestCase):

	def test_defaults(t):
		t.assertNotEqual(config.SECRET_KEY(), '')
		t.assertFalse(config.DEBUG())
		t.assertListEqual(config.ALLOWED_HOSTS(), ['localhost'])
		t.assertEqual(config.DBDIR().as_posix(), '/var/opt/uwsapp')
		t.assertEqual(config.DBNAME(), 'app.db')
		t.assertEqual(config._url_base, '')

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

if __name__ == '__main__':
	unittest.main()
