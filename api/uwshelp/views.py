# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.views.generic import TemplateView

class Index(TemplateView):
	template_name = 'uwshelp/index.html'
	http_method_names = ['get', 'head']

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'index'
		return d

class Help(TemplateView):
	template_name = 'uwshelp/doc.html'
	http_method_names = ['get', 'head']
	__path = ''

	def dispatch(v, req, *args, **kwargs):
		v.__path = kwargs.get('path', '')
		return super().dispatch(req, *args, **kwargs)

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = v.__path
		return d
