# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapi.views import ApiView

from uwsapp import log

from . import nqlog
from . import syslog

#
# Index
#

class Index(ApiView):

	def post(v, req, name = '') -> JsonResponse:
		try:
			if name == 'app-ctl':
				return v.uwsapi_resp(syslog.app_ctl().all())
			if name == 'uwsq':
				return v.uwsapi_resp(syslog.uwsq().all())
		except Exception as err:
			log.error(err)
			return v.uwsapi_internal_error()
		return v.uwsapi_bad_request()

#
# NQ
#

class NQ(ApiView):

	def post(v, req) -> JsonResponse:
		try:
			return v.uwsapi_resp(nqlog.jobs().all())
		except Exception as err:
			log.error(err)
		return v.uwsapi_internal_error()

#
# NQTail
#

class NQTail(ApiView):

	def post(v, req, jobid = '') -> JsonResponse:
		try:
			job = nqlog.tail(jobid)
		except nqlog.NotFound as err:
			log.error(err)
			return v.uwsapi_not_found()
		except Exception as err:
			log.error(err)
			return v.uwsapi_internal_error()
		d = v.uwsapi_resp({})
		d['job'] = job
		return d
