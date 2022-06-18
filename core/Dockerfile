FROM uwsapp/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsops -m 0750 /opt/uwsapp/core
COPY --chown=uws:uwsops ./ /opt/uwsapp/core/
RUN rm -vf /opt/uwsapp/core/Dockerfile /opt/uwsapp/core/.dockerignore

USER uws:uwsops

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/core

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/sbin/nologin
