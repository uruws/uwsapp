# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from contextlib    import contextmanager
from unittest.mock import MagicMock

from http import HTTPStatus

from uwsapi.views_test import ApiViewTestCase

from uwslogs import nqlog

@contextmanager
def mock_run(status = 0, output = 'mock_output'):
	bup = nqlog._run
	try:
		nqlog._run = MagicMock(return_value = (status, output))
		yield
	finally:
		nqlog._run = bup

class NqlogTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/logs/nq/index', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertIsInstance(resp.json(), dict)

	def test_run_error(t):
		with mock_run(status = 99):
			t.assertTrue(nqlog._jobfail('/run/uwscli/nq/,1823af52ff8.17752'))
		with mock_run(status = 99):
			t.assertIsNotNone(nqlog.jobs())

	def test_jobinfo_error(t):
		e = nqlog.JobEntry('invalid.id')
		nqlog._jobinfo(e, 'testing')

	def test_jobs_invalid_id(t):
		i = nqlog.JobsInfo()
		h = ['==> , <==']
		nqlog._jobs(i, h)
		t.assertEqual(len(i), 0)

	def test_jobs_chdir_error(t):
		i = nqlog.jobs(nqdir = '/not.found')
		t.assertEqual(len(i), 0)

class NqlogTailTest(ApiViewTestCase):

	def test_index(t):
		resp = t.uwsapi_post('/logs/nq/1823af52426.17746/tail', {})
		t.assertEqual(resp.status_code, HTTPStatus.OK)
		t.assertDictEqual(resp.json(), {
			'jid':   '1823af52426.17746',
			'lines': '100',
			'rows':  3,
			'tail':  'INTERNAL ERROR [-128]: exec nq -c sleep 60',
		})

	def test_not_found(t):
		resp = t.uwsapi_post('/logs/nq/invalid/tail', {})
		t.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
		t.assertDictEqual(resp.json(), {})

	def test_job_tail_string(t):
		j = nqlog.JobTail('testing.fn', 999)
		t.assertEqual(str(j), 'testing.fn')

	def test_job_tail_error(t):
		try:
			nqlog._tail_cmd = '/bin/false'
			j = nqlog.JobTail('testing.fn', 999)
			t.assertEqual(j.tail(), 'INTERNAL ERROR [1]: ')
		finally:
			nqlog._tail_cmd = '/usr/bin/tail'
