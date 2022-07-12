# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.conf          import settings
from django.views.generic import TemplateView

from markdown2 import markdown_path # type: ignore

from uwsapp import log

def _docslist() -> list[str]:
	docsdir = settings.BASE_DIR / 'docs'
	return list(sorted([fn.as_posix().replace(docsdir.as_posix(), '', 1)[1:-3] for fn in docsdir.rglob('*.md')]))

class Index(TemplateView):
	template_name = 'uwshelp/index.html'
	http_method_names = ['get', 'head']

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title'] = 'index'
		d['docs'] = _docslist()
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
