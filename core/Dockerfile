FROM uwsapp/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

COPY --chown=uws:uwsops ./ /opt/uwsapp/core/
RUN rm -vf /opt/uwsapp/core/Dockerfile /opt/uwsapp/core/.dockerignore

USER uws:uws

ENV USER uws
ENV HOME /home/uws

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/sbin/nologin
