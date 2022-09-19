# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from time import time

from django.views.generic import TemplateView

from django.utils.decorators       import method_decorator
from django.views.decorators.cache import cache_control

from uwsapp import config

@method_decorator(
	cache_control(**config.CACHE_CONTROL()),
	name = 'dispatch',
)
class WBView(TemplateView):

	def uwswb_data(v, d):
		return d

class Index(WBView):
	template_name = 'uwswb/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'whistle blower'
		return v.uwswb_data(d)
