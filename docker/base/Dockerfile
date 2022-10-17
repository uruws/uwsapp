FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220711"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN groupadd -o -g 3000 uwsapp \
	&& useradd -o -d /home/uwsapp -m -c 'uwsapp' -g 3000 -u 3000 uwsapp \
	&& chmod -v 0750 /home/uwsapp

RUN /root/bin/apt-install.sh python3 uwsgi-plugin-python3 \
	pwgen sqlite3 python3-django python3-markdown2 nq

RUN /usr/bin/python3 -m django --version

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp \
	&& install -v -d -o uws -g uwsapp -m 0750 /var/opt/uwsapp

USER uwsapp:uwsapp
WORKDIR /home/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENV UWSAPP_HOME /opt/uwsapp
ENV UWSAPP_PORT 3000
ENV UWSAPP_WORKERS 3
ENV PYTHONPATH /opt/uwsapp/core
ENV LANG es_US.UTF-8
ENV LANGUAGE es_US.UTF-8
ENV LC_ALL es_US.UTF-8
ENV LC_CTYPE UTF-8
ENV PYTHONUTF8 1
ENV PYTHONIOENCODING utf-8

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ENV UWSAPP_HOME /opt/uwsapp
ENV UWSAPP_PORT 3000
ENV UWSAPP_WORKERS 3
ENV PYTHONPATH /opt/uwsapp/core
ENV LANG es_US.UTF-8
ENV LANGUAGE es_US.UTF-8
ENV LC_ALL es_US.UTF-8
ENV LC_CTYPE UTF-8
ENV PYTHONUTF8 1
ENV PYTHONIOENCODING utf-8

COPY --chown=uws:uwsapp ./bin/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod -v 0750  /usr/local/bin/entrypoint.sh

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/sbin/nologin
