#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import ssl

from contextlib import contextmanager

from uwsapp import api
from uwsapp import config

bup_urlopen = api.urlopen

class Test(unittest.TestCase):

	def setUp(t):
		api.urlopen = MagicMock(return_value = None)
		t.cli = api.ApiClient()

	def tearDown(t):
		api.urlopen = bup_urlopen

	@contextmanager
	def mock_req(t):
		bup = t.cli._req
		try:
			t.cli._req = MagicMock(return_value = None)
			yield
		finally:
			t.cli._req = bup

	def test_defaults(t):
		t.assertTrue(t.cli.ctx.check_hostname)
		t.assertEqual(t.cli.ctx.verify_mode, ssl.CERT_REQUIRED)

	def test_debug_config(t):
		bup = config.DEBUG
		try:
			config.DEBUG = MagicMock(return_value = True)
			cli = api.ApiClient()
			t.assertFalse(cli.ctx.check_hostname)
			t.assertEqual(cli.ctx.verify_mode, ssl.CERT_NONE)
		finally:
			config.DEBUG = bup

	def test_certfile_config(t):
		bup = config.API_CERTFILE
		try:
			config.API_CERTFILE = MagicMock(return_value = 'lalala')
			cli = api.ApiClient()
		finally:
			config.API_CERTFILE = bup

	def test_POST(t):
		t.cli.POST('/testing', {'test': 'ing'})
		api.urlopen.assert_called_once()

	def test_POST_req(t):
		with t.mock_req():
			t.cli.POST('/testing', {'test': 'ing'})
			api.urlopen.assert_called_once()
			t.cli._req.assert_called_once_with('/testing', {'test': 'ing'})

if __name__ == '__main__':
	unittest.main()
