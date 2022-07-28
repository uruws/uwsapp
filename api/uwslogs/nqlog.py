# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from collections import deque
from os          import chdir
from subprocess  import getstatusoutput
from typing      import Optional

from uwsapp import config
from uwsapp import log

class JobEntry(object):
	jid:       str  = ''
	running:   bool = False
	failed:    bool = False
	start:     str  = ''
	end:       str  = ''

class JobsInfo(deque):

	def _pop(q):
		i = q.pop()
		return {
			"jid":     i.jid,
			"running": i.running,
			"failed":  i.failed,
			"start":   i.start,
			"end":     i.end,
		}

	def all(q):
		d = {}
		for i in range(len(q)):
			d[i] = q._pop()
		return d

def _run(cmd) -> tuple[int, str]:
	return getstatusoutput(cmd)

def _jobs(j: JobsInfo, heads: list[str]) -> Optional[JobsInfo]:
	for line in heads:
		if line.startswith('==> ,') and line.endswith(' <=='):
			jid = line.split(',', maxsplit = 2)[1][:-4]
			log.debug('nq job id:', jid)

def jobs() -> JobsInfo:
	i = JobsInfo()
	dn = config.CLI_NQDIR()
	log.debug('nq dir:', dn)
	chdir(dn)
	st, heads = _run('/usr/bin/head -n1 ,*.*')
	if st != 0:
		log.error(f"jobs head: exit status {st}")
		return i
	_jobs(i, heads.splitlines())
	return i
