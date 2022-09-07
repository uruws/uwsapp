# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.http import JsonResponse

from uwsapp import log
from uwsapp import user

from uwsapi.views import ApiView

#
# Index
#

class Index(ApiView):

	def post(v, req) -> JsonResponse:
		try:
			return v.uwsapi_resp(user.apps(v.uwsapi_username()))
		except user.Error as err:
			log.error(err)
			return v.uwsapi_internal_error()

#
# App Info
#

class AppInfo(ApiView):

	def post(v, req, name):
		log.debug('app:', name)
		try:
			apps = user.apps(v.uwsapi_username())
		except user.Error as err:
			log.error(err)
			return v.uwsapi_internal_error()
		d = apps.get('deploy', {}).get(name, {})
		if not d:
			log.error(f"app {name}: not found")
			return v.uwsapi_bad_request({})
		d['name'] = name
		return v.uwsapi_resp(d)
