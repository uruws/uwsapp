# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from django.test   import TestCase
from subprocess    import CalledProcessError
from unittest.mock import MagicMock

from uwsapp import config
from uwsapp import log_test

from uwscmd import cmd

__bup_sshcmd = cmd._sshcmd

def mock_setup():
	log_test.mock_setup()
	cmd._sshcmd = MagicMock(return_value = '/opt/uwsapp/_devel/api/uwscmd/sshcmd.sh')

def mock_teardown():
	cmd._sshcmd = __bup_sshcmd
	log_test.mock_teardown()

@contextmanager
def mock_execute():
	try:
		mock_setup()
		yield
	finally:
		mock_teardown()

class ApiCmdTest(TestCase):

	def test_setenv(t):
		dbg = 'on'
		if not config.DEBUG():
			dbg = 'off'
		t.assertDictEqual(cmd._setenv('testing'), {
			'HOME':              '/home/uws',
			'HOSTNAME':          'devel.uwsapp.local',
			'PATH':              '/usr/bin:/bin:/usr/local/bin',
			'TZ':                'UTC',
			'USER':              'uws',
			'UWSAPP_DEBUG':      dbg,
			'UWSAPP_CLI_HOST':   'localhost',
			'UWSAPP_CLI_SSHCMD': '/usr/bin/ssh',
			'UWSAPP_HOME':       '/opt/uwsapp',
			'UWSAPP_LOG':        '',
			'UWSAPP_USER':       'testing',
		})

	def test_check_output(t):
		st, out = cmd._check_output('testing', '/bin/true')
		t.assertEqual(st, 'ok')
		t.assertEqual(out, '')

	def test_check_output_error(t):
		st = '__ERROR__'
		out = '__FAIL__'
		st, out = cmd._check_output('testing', '/bin/false')
		t.assertEqual(st, 'error')
		t.assertEqual(out, '')

	def test_execute(t):
		d = cmd.execute('testing', 'test', 'appt', command = '/bin/true')
		t.assertDictEqual(d,
			{'command': '/bin/true', 'output': '', 'status': 'ok'})

	def test_execute_error(t):
		with mock_execute():
			d = cmd.execute('testing', 'test', 'appt', command = '/bin/false')
			t.assertDictEqual(d,
				{'command': '/bin/false', 'output': '', 'status': 'error'})
