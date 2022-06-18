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

USER uws:uws

ENV USER uws
ENV HOME /home/uws

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/local/bin/entrypoint.sh
