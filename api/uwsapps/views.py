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
		username = v.uwsapi_username()
		log.debug('app:', name)
		log.debug('username:', username)
		try:
			apps = user.apps(username)
		except user.Error as err:
			log.error(username, err)
			return v.uwsapi_internal_error()
		d = apps.get('deploy', {}).get(name, {})
		if not d:
			log.error(f"{username} app {name}: not found")
			return v.uwsapi_bad_request({})
		d['name'] = name
		d['commands'] = []
		for cmd in apps.get('commands', []):
			if cmd.startswith('app-'):
				d['commands'].append(cmd[4:])
		return v.uwsapi_resp(d)
