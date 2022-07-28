# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsapp.api import ApiClient
from uwsapp.api import ApiError

from uwsweb.views import WebView

class NQ(WebView):
	template_name = 'uwslogs/nq.html'
	_cli          = None

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		if v._cli is None:
			v._cli = ApiClient(session = v.uwsapi_session())

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'jobs'
		d['title_desc'] = 'Jobs Queue'
		try:
			d['nqlog']     = v._jobs()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
		return v.uwsweb_data(d)

	def _jobs(v):
		resp = v._cli.POST('/logs/nq/index', {})
		return v._cli.parse(resp)

class AppCtl(WebView):
	template_name = 'uwslogs/index.html'
	_cli          = None

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		if v._cli is None:
			v._cli = ApiClient(session = v.uwsapi_session())

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'app-ctl'
		d['title_desc'] = 'App Control'
		try:
			d['syslog']     = v._app_ctl()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
		return v.uwsweb_data(d)

	def _app_ctl(v):
		resp = v._cli.POST('/logs/app-ctl', {})
		return v._cli.parse(resp)

class Uwsq(WebView):
	template_name = 'uwslogs/index.html'
	_cli          = None

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		if v._cli is None:
			v._cli = ApiClient(session = v.uwsapi_session())

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'uwsq'
		d['title_desc'] = 'Build Queue'
		try:
			d['syslog']     = v._uwsq()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
		return v.uwsweb_data(d)

	def _uwsq(v):
		resp = v._cli.POST('/logs/uwsq', {})
		return v._cli.parse(resp)
