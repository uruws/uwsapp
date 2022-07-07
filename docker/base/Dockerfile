FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220523"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh python3 uwsgi-plugin-python3 \
	pwgen sqlite3 python3-django python3-markdown2 nq

RUN /usr/bin/python3 -m django --version

RUN install -v -d -o uws -g uwsops -m 0750 /opt/uwsapp \
	&& install -v -d -o uws -g uwsops -m 0750 /var/opt/uwsapp \
	&& install -v -d -o uws -g uwsops -m 0750 /run/uwsapp \
	&& install -v -d -o uws -g uwsops -m 0750 /run/uwscli

USER uwsops:uwsops
WORKDIR /home/uwsops

ENV USER uwsops
ENV HOME /home/uwsops

ENV UWSAPP_HOME /opt/uwsapp
ENV UWSAPP_PORT 3000
ENV UWSAPP_WORKERS 3
ENV PYTHONPATH /opt/uwsapp/core

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ENV UWSAPP_HOME /opt/uwsapp
ENV UWSAPP_PORT 3000
ENV UWSAPP_WORKERS 3
ENV PYTHONPATH /opt/uwsapp/core

COPY --chown=uws:uwsops ./bin/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod -v 0750  /usr/local/bin/entrypoint.sh

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/sbin/nologin
