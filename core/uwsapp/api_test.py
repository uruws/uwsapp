#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

from contextlib import contextmanager

from uwsapp import api

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
