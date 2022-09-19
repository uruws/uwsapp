FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220919"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsapp -m 0750 /run/uwswb

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp/wb
COPY --chown=uws:uwsapp ./ /opt/uwsapp/wb/
RUN rm -vf /opt/uwsapp/wb/Dockerfile /opt/uwsapp/wb/.dockerignore

USER uws:uwsapp
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/wb

USER uwsapp:uwsapp
WORKDIR /opt/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENV UWSAPP_NAME wb
ENV UWSAPP_URL wb/

ENTRYPOINT /usr/local/bin/entrypoint.sh
