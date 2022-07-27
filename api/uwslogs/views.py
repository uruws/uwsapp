# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapi.views import ApiView

from . import nqlog
from . import syslog

class Index(ApiView):

	def post(v, req, name = '') -> JsonResponse:
		if name == 'app-ctl':
			return v.uwsapi_resp(syslog.app_ctl().all())
		if name == 'uwsq':
			return v.uwsapi_resp(syslog.uwsq().all())
		return v.uwsapi_bad_request()

class NQ(ApiView):

	def post(v, req, jobid = '') -> JsonResponse:
		if name == 'index':
			return v.uwsapi_resp(nqlog.jobs().all())
		return v.uwsapi_bad_request()
