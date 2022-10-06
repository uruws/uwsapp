FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsapp -m 0750 /run/uwsapi \
	&& install -v -d -o uws -g uwsapp -m 0750 /run/uwsweb \
	&& install -v -d -o uws -g uwsapp -m 0750 /run/uwscli \
	&& install -v -d -o uws -g uwsapp -m 0750 /run/uwscli/syslog

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp/web
COPY --chown=uws:uwsapp ./ /opt/uwsapp/web/
RUN rm -vf /opt/uwsapp/web/Dockerfile /opt/uwsapp/web/.dockerignore

USER uws:uwsapp
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/web

USER uwsapp:uwsapp
WORKDIR /opt/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENV UWSAPP_NAME web
ENV UWSAPP_URL web/

ENTRYPOINT /usr/local/bin/entrypoint.sh
