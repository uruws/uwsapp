#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib import contextmanager

import unittest
from unittest.mock import MagicMock

from io import StringIO

from uwsapp import config
from uwsapp import log

_bup_outfh = log._outfh
_bup_errfh = log._errfh

def mock_setup():
	if not config.DEBUG():
		log._outfh = StringIO()
		log._errfh = StringIO()

def mock_teardown():
	if not config.DEBUG():
		log._outfh = _bup_outfh
		log._errfh = _bup_errfh

@contextmanager
def mock():
	try:
		mock_setup()
		yield
	finally:
		mock_teardown()

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

	def test_mock(t):
		with mock():
			log.print('test mock')

	def _out(t):
		return log._outfh.getvalue().strip()

	def _err(t):
		return log._errfh.getvalue().strip()

	def test_print(t):
		log.print('testing', '...')
		t.assertEqual(t._out(), 'testing ...')
		t.assertEqual(t._err(), '')

	def test_debug(t):
		if not config.DEBUG():
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
