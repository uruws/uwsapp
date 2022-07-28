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
	command:   str  = ''

	def __init__(e, jid: str):
		e.jid = jid

class JobsInfo(deque):

	def _pop(q):
		i = q.pop()
		return {
			"jid":     i.jid,
			"running": i.running,
			"failed":  i.failed,
			"start":   i.start,
			"end":     i.end,
			"command": i.command,
		}

	def all(q):
		d = {}
		for i in range(len(q)):
			d[i] = q._pop()
		return d

def _run(cmd) -> tuple[int, str]:
	return getstatusoutput(cmd)

def _jobinfo(j: JobEntry):
	log.debug('job info:', j.jid)

def _jobs(i: JobsInfo, heads: list[str]) -> Optional[JobsInfo]:
	j = None
	for line in heads:
		jid = ''
		line = line.strip()
		if line == '':
			continue
		if line.startswith('==> ,') and line.endswith(' <=='):
			jid = line.split(',', maxsplit = 2)[1][:-4].strip()
			log.debug('nq job id:', jid)
			if jid != '':
				if j is not None:
					i.append(j)
				j = None
			else:
				continue
		if j is None:
			j = JobEntry(jid)
		else:
			_jobinfo(j)
	if j is not None:
		i.append(j)

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
