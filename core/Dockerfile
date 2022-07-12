FROM uwsapp/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp/core
COPY --chown=uws:uwsapp ./ /opt/uwsapp/core/
RUN rm -vf /opt/uwsapp/core/Dockerfile /opt/uwsapp/core/.dockerignore

USER uws:uwsapp
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/core

USER uwsapp:uwsapp
WORKDIR /opt/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENTRYPOINT /usr/sbin/nologin
