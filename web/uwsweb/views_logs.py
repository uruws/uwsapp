# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.shortcuts import render

from uwsapp.api import ApiClient

from uwsweb.views import WebView

class AppCtl(WebView):
	template_name = 'uwslogs/index.html'
	_cli          = None

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		if v._cli is None:
			v._cli = ApiClient(session = v.uwsapi_session())

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'syslog'
		d['title_desc'] = 'app-ctl.log'
		d['syslog']     = v._app_ctl()
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
		d['title_desc'] = 'uwsq.log'
		d['syslog']     = v._uwsq()
		return v.uwsweb_data(d)

	def _uwsq(v):
		resp = v._cli.POST('/logs/uwsq', {})
		return v._cli.parse(resp)
