# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapp import log
from uwsapp import user

from uwsapi.views import ApiView

class Index(ApiView):

	def post(v, req) -> JsonResponse:
		try:
			return v.uwsapi_resp(user.apps(v.uwsapi_username()))
		except user.Error as err:
			log.error(err)
			return v.uwsapi_internal_error()
