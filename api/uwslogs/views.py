# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapi.views import ApiView

from uwsapp import log

from . import nqlog
from . import syslog

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

class NQ(ApiView):

	def post(v, req, jobid = '') -> JsonResponse:
		try:
			if jobid == 'index':
				return v.uwsapi_resp(nqlog.jobs().all())
		except Exception as err:
			log.error(err)
			return v.uwsapi_internal_error()
		return v.uwsapi_bad_request()
