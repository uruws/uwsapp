# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.test import TestCase

from uwscmd import cmd

class ApiCmdTest(TestCase):

	def test_setenv(t):
		t.assertDictEqual(cmd._setenv('testing'), {
			'HOME':         '/home/uws',
			'HOSTNAME':     'devel.uwsapp.local',
			'PATH':         '/usr/local/bin:/usr/bin:/bin',
			'USER':         'uws',
			'UWSAPP_DEBUG': 'off',
			'UWSAPP_HOME':  '/opt/uwsapp',
			'UWSAPP_LOG':   '',
			'UWSAPP_USER':  'testing',
		})
