#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

from uwsapp import config
from uwsapp import user

class Test(unittest.TestCase):

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

if __name__ == '__main__':
	unittest.main()
