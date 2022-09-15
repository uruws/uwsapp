# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from uwsapp import config

from uwsweb.views import ApiError
from uwsweb.views import WebView

#
# nq
#

class NQ(WebView):
	template_name = 'uwslogs/nq.html'
	__url         = config.apiurl('logs-nq-index', '/logs/nq/index')

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'jobs'
		d['title_desc'] = 'Jobs Queue'
		try:
			d['nqlog'] = v._jobs()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['nqlog'] = {}
		return v.uwsweb_data(d)

	def _jobs(v): # pragma: no cover
		resp = v.uwsapi_post(v.__url, {})
		return v.uwsapi_parse_response(resp)

#
# nq tail
#

class NQTail(WebView):
	template_name = 'uwslogs/nq-tail.html'
	__url         = config.apiurl('logs-nq-tail', '/logs/nq/{jobid}/tail')
	__lines       = '100'

	def dispatch(v, req, *args, **kwargs):
		v.__lines = req.GET.get('lines', '100')
		return super().dispatch(req, *args, **kwargs)

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		jobid = kwargs.get('jobid', '')
		if jobid == '': # pragma: no cover
			log.error('no jobid')
			return v.uwsapi_bad_request({})
		d['navbar_id']  = 'jobs'
		d['title']      = f"job {jobid}"
		d['title_desc'] = f"Job: {jobid}"
		try:
			d['job'] = v._job(jobid, v.__lines)
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['job'] = {}
		return v.uwsweb_data(d)

	def _job(v, jobid, lines): # pragma: no cover
		resp = v.uwsapi_post(v.__url.format(jobid = jobid), {'lines': lines})
		return v.uwsapi_parse_response(resp)

#
# app-ctl
#

class AppCtl(WebView):
	template_name = 'uwslogs/index.html'
	__url         = config.apiurl('logs-app-ctl', '/logs/app-ctl')

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['navbar_id']  = 'ctl'
		d['title']      = 'app-ctl'
		d['title_desc'] = 'App Control'
		try:
			d['syslog'] = v._app_ctl()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['syslog'] = {}
		return v.uwsweb_data(d)

	def _app_ctl(v): # pragma: no cover
		resp = v.uwsapi_post(v.__url, {})
		return v.uwsapi_parse_response(resp)

#
# uwsq
#

class Uwsq(WebView):
	template_name = 'uwslogs/index.html'
	__url         = config.apiurl('logs-uwsq', '/logs/uwsq')

	def get_context_data(v, **kwargs):
		d = super().get_context_data(**kwargs)
		d['title']      = 'uwsq'
		d['title_desc'] = 'Build Queue'
		try:
			d['syslog'] = v._uwsq()
		except ApiError as err:
			v.uwsweb_msg_error(str(err))
			d['syslog'] = {}
		return v.uwsweb_data(d)

	def _uwsq(v): # pragma: no cover
		resp = v.uwsapi_post(v.__url, {})
		return v.uwsapi_parse_response(resp)
