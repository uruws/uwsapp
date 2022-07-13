# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.utils.timezone import now
from django.views.generic  import TemplateView

class WebView(TemplateView):
	http_method_names = ['get', 'head']

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['now'] = now()
		return d

class Index(WebView):
	template_name = 'uwsweb/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'index'
		return d
