# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from django.shortcuts import render

def index(req):
	return render(req, 'uwsweb/index.html')
