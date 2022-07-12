# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

"""uwsapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls    import include
from django.urls    import path

from uwsapp.config import URL

from . import cmd
from . import views

urlpatterns = [
	path(URL('exec/<slug:name>'), cmd.view, name = 'exec'),
	path(URL('auth/'), include('uwsauth.urls')),
	path(URL('admin/'), admin.site.urls),
	path(URL(''), views.index, name = 'index'),
]

handler404 = 'uwsapi.views.error404'
