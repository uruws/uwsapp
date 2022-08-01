#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest
from unittest.mock import MagicMock

from io import StringIO

from uwsapp import log

_bup_outfh = log._outfh
_bup_errfh = log._errfh

class Test(unittest.TestCase):

	def setUp(t):
		log._outfh = StringIO()
		log._errfh = StringIO()

	def tearDown(t):
		log._outfh = _bup_outfh
		log._errfh = _bup_errfh
		log._log   = True
		log._debug = False

	def test_defaults(t):
		t.assertTrue(log._log)
		t.assertFalse(log._debug)

	def _out(t):
		return log._outfh.getvalue().strip()

	def _err(t):
		return log._errfh.getvalue().strip()

	def test_print(t):
		log.print('testing', '...')
		t.assertEqual(t._out(), 'testing ...')
		t.assertEqual(t._err(), '')

	def test_debug(t):
		log.debug('t0')
		t.assertEqual(t._out(), '')
		t.assertEqual(t._err(), '')
		log._debug = True
		log.debug('testing', '...')
		t.assertEqual(t._err(), '')
		t.assertTrue(t._out().startswith(f"{__file__}:test_debug:"))
		t.assertTrue(t._out().endswith('testing ...'))

	def test_error(t):
		log.error('testing', '...')
		t.assertEqual(t._err(), '[ERROR] testing ...')
		t.assertEqual(t._out(), '')

if __name__ == '__main__':
	unittest.main()
