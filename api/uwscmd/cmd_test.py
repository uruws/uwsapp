# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from subprocess import CalledProcessError

from uwscmd import cmd

class ApiCmdTest(TestCase):

	def test_setenv(t):
		t.assertDictEqual(cmd._setenv('testing'), {
			'HOME':          '/home/uws',
			'HOSTNAME':      'devel.uwsapp.local',
			'PATH':          '/usr/local/bin:/usr/bin:/bin',
			'USER':          'uws',
			'UWSAPP_DEBUG':  'off',
			'UWSAPP_HOME':   '/opt/uwsapp',
			'UWSAPP_LOG':    '',
			'UWSAPP_SSHCMD': '/usr/bin/ssh',
			'UWSAPP_USER':   'testing',
		})

	def test_check_output(t):
		out = cmd._check_output('testing', '/bin/true')
		t.assertEqual(out, '')

	def test_check_output_error(t):
		with t.assertRaises(CalledProcessError):
			out = cmd._check_output('testing', '/bin/false')
			t.assertEqual(out, '')

	def test_execute(t):
		d = cmd.execute('testing', 'test', 'appt', command = '/bin/true')
		t.assertDictEqual(d,
			{'command': '/bin/true', 'output': '', 'status': 'ok'})

	def test_execute_error(t):
		d = cmd.execute('testing', 'test', 'appt', command = '/bin/false')
		t.assertDictEqual(d,
			{'command': '/bin/false', 'output': '', 'status': 'error'})
