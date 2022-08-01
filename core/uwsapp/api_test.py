#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

import ssl

from contextlib import contextmanager
from io         import StringIO

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
			config.API_CERTFILE = MagicMock(return_value = 'testing')
			cli = api.ApiClient()
		finally:
			config.API_CERTFILE = bup

	def test_url(t):
		t.assertEqual(config.API_HOST(), 'localhost')
		t.assertEqual(config.API_PORT(), '443')
		t.assertEqual(t.cli._url('/testing'), 'https://localhost:443/api/testing')

	def test_session(t):
		t.assertIsNone(t.cli._sess)
		cli = api.ApiClient(session = 'testing')
		t.assertEqual(cli._sess, 'testing')

	def test_POST(t):
		t.cli.POST('/testing', {'test': 'ing'})
		api.urlopen.assert_called_once()

	def test_POST_req(t):
		with t.mock_req():
			t.cli.POST('/testing', {'test': 'ing'})
			api.urlopen.assert_called_once()
			t.cli._req.assert_called_once_with('/testing', {'test': 'ing'})

	def test_POST_session(t):
		t.cli = api.ApiClient(session = 'testing')
		with t.mock_req():
			t.cli.POST('/testing', {'test': 'ing'})
			api.urlopen.assert_called_once()
			t.cli._req.assert_called_once_with('/testing',
				{'test': 'ing', 'session': 'testing'})

	def test_POST_error(t):
		def _error(*args, **kwargs):
			raise Exception('testing')
		api.urlopen = MagicMock(side_effect = _error)
		with t.assertRaises(api.ApiError):
			t.cli.POST('/testing', {'test': 'ing'})

	def test_parse_resp(t):
		resp = StringIO('{}')
		d = t.cli.parse(resp)
		t.assertTrue(isinstance(d, dict))
		t.assertEqual(d, {})

	def test_parse_resp_error(t):
		resp = StringIO()
		with t.assertRaises(api.ApiError):
			t.cli.parse(resp)

if __name__ == '__main__':
	unittest.main()
