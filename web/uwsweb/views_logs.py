# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.shortcuts import render

from uwsapp.api import ApiClient

from uwsweb.views import WebView

class Syslog(WebView):
	template_name = 'uwslogs/index.html'
	_cli          = None

	def setup(v, req, *args, **kwargs):
		super().setup(req, *args, **kwargs)
		if v._cli is None:
			v._cli = ApiClient(session = v.uwsapi_session())

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'syslog'
		d['title_desc'] = 'System Log: uwsq'
		d['syslog']     = v._uwsq()
		return v.uwsweb_data(d)

	def _uwsq(v):
		resp = v._cli.POST('/logs/uwsq', {})
		return v._cli.parse(resp)
