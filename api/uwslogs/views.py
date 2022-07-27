# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapi.views import ApiView

from . import syslog

class Index(ApiView):

	def post(v, req, name = '') -> JsonResponse:
		if name == 'nq':
			return v.uwsapi_resp(syslog.jobs().all())
		if name == 'app-ctl':
			return v.uwsapi_resp(syslog.app_ctl().all())
		if name == 'uwsq':
			return v.uwsapi_resp(syslog.uwsq().all())
		return v.uwsapi_bad_request()
