# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.conf          import settings
from django.views.generic import TemplateView

from django.utils.decorators       import method_decorator
from django.views.decorators.cache import cache_control

from markdown2 import markdown_path # type: ignore

from uwsapp import log

@method_decorator(
	cache_control(max_age = 5, must_revalidate = True, private = True, stale_if_error = True),
	name = 'dispatch',
)
class HelpView(TemplateView):
	http_method_names = ['get', 'head']

#
# Index
#

class Index(HelpView):
	template_name = 'uwshelp/index.html'

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'index'
		d['api_docs'] = _docslist('api')
		d['web_docs'] = _docslist('web')
		return d

def _docslist(section: str) -> list[str]:
	docsdir = settings.BASE_DIR / 'docs' / section
	return list(sorted([f"{section}/{fn.as_posix().replace(docsdir.as_posix(), '', 1)[1:-3]}" for fn in docsdir.rglob('*.md')]))

#
# Help
#

class Help(HelpView):
	template_name = 'uwshelp/doc.html'
	__path = ''

	def dispatch(v, req, *args, **kwargs):
		v.__path = kwargs.get('path', '')
		return super().dispatch(req, *args, **kwargs)

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = '/%s' % v.__path
		d['doc'] = _markdown(v.__path)
		return d

def _markdown(path: str) -> str:
	doc = 'EMPTY'
	fn = settings.BASE_DIR / 'docs' / str('%s.md' % path)
	try:
		doc = markdown_path(fn)
	except Exception as err:
		log.error(err)
		doc = '<pre class="w3-container w3-red">ERROR: %s</pre>' % str(err)
	return doc
