# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.views.generic import TemplateView

class Index(TemplateView):
	template_name = 'uwspop/index.html'
