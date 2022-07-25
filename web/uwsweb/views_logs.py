# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.shortcuts import render

from uwsweb.views import WebView

class Syslog(WebView):
	template_name = 'uwslogs/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'syslog'
		d['title_desc'] = 'System Log'
		return v.uwsweb_data(d)
