# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapi.views import ApiView

from uwsapp import log

from uwscmd import cmd

class Index(ApiView):

	def post(v, req) -> JsonResponse:
		try:
			command = req.POST['command']
			app = req.POST['app']
		except KeyError as err:
			log.error(err)
			return v.uwsapi_bad_request()
		data = cmd.execute(req.user.username, command, app)
		return v.uwsapi_resp(data)
