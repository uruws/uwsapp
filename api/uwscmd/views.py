# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapi.views import ApiView

class Index(ApiView):

	def post(v, req, name) -> JsonResponse:
		return v.uwsapi_resp({'command': name})
