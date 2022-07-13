#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

from uwsapp import api

bup_urlopen = api.urlopen

class Test(unittest.TestCase):

	def setUp(t):
		api.urlopen = MagicMock(return_value = None)
		t.cli = api.ApiClient()

	def tearDown(t):
		api.urlopen = bup_urlopen

	def test_POST(t):
		t.cli.POST('/testing', {'test': 'ing'})

if __name__ == '__main__':
	unittest.main()
