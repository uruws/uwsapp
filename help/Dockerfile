FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220711"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp/help
COPY --chown=uws:uwsapp ./ /opt/uwsapp/help/
RUN rm -vf /opt/uwsapp/help/Dockerfile /opt/uwsapp/help/.dockerignore

USER uws:uwsapp
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/help

USER uwsapp:uwsapp
WORKDIR /opt/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENV UWSAPP_NAME help
ENV UWSAPP_URL help/

ENTRYPOINT /usr/local/bin/entrypoint.sh
