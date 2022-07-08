FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsops -m 0750 /opt/uwsapp/api
COPY --chown=uws:uwsops ./ /opt/uwsapp/api/
RUN rm -vf /opt/uwsapp/api/Dockerfile /opt/uwsapp/api/.dockerignore

USER uws:uwsops
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/api

ENV UWSAPP_NAME api
ENV UWSAPP_URL api/

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/local/bin/entrypoint.sh
