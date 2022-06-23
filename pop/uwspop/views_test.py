# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from os import environ

from django.test import TestCase

from uwsapp import config

from uwspop import views

class PopViewsTests(TestCase):

	def test_loadenv_defaults(t):
		t.assertEqual(views._hostname, 'localhost')
		t.assertEqual(views._port, 995)
		t.assertEqual(views._timeout, 15)
		t.assertEqual(views._lmax, 100)

	def test_loadenv(t):
		try:
			environ['UWSPOP_HOSTNAME'] = 'thost'
			environ['UWSPOP_PORT'] = '123'
			environ['UWSPOP_TIMEOUT'] = '20'
			environ['UWSPOP_LIST_MAX'] = '3'
			views._loadenv()
			t.assertEqual(views._hostname, 'thost')
			t.assertEqual(views._port, 123)
			t.assertEqual(views._timeout, 20)
			t.assertEqual(views._lmax, 3)
		finally:
			views._hostname = 'localhost'
			views._port = 995
			views._timeout = 15
			views._lmax = 100

	def test_loadenv_error(t):
		try:
			environ['UWSPOP_PORT'] = 'test_error'
			with t.assertRaises(RuntimeError):
				views._loadenv()
			t.assertEqual(views._hostname, 'thost')
			t.assertEqual(views._port, 995)
		finally:
			views._port = 995
