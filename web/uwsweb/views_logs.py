# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsweb.views import ApiError
from uwsweb.views import WebView

class NQ(WebView):
	template_name = 'uwslogs/nq.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'jobs'
		d['title_desc'] = 'Jobs Queue'
		try:
			d['nqlog'] = v._jobs()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['nqlog'] = {}
		return v.uwsweb_data(d)

	def _jobs(v): # pragma: no cover
		resp = v.uwsapi_post('/logs/nq/index', {})
		return v.uwsapi_parse_response(resp)

class AppCtl(WebView):
	template_name = 'uwslogs/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'app-ctl'
		d['title_desc'] = 'App Control'
		try:
			d['syslog'] = v._app_ctl()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['syslog'] = {}
		return v.uwsweb_data(d)

	def _app_ctl(v): # pragma: no cover
		resp = v.uwsapi_post('/logs/app-ctl', {})
		return v.uwsapi_parse_response(resp)

class Uwsq(WebView):
	template_name = 'uwslogs/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'uwsq'
		d['title_desc'] = 'Build Queue'
		try:
			d['syslog'] = v._uwsq()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['syslog'] = {}
		return v.uwsweb_data(d)

	def _uwsq(v): # pragma: no cover
		resp = v.uwsapi_post('/logs/uwsq', {})
		return v.uwsapi_parse_response(resp)
