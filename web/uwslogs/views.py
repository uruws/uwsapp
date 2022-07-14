# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.shortcuts import render

from uwsweb.views import WebView

class Index(WebView):
	template_name = 'uwsweb/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		return v.uwsweb_data(d)
