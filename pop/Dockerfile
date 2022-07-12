FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp/pop
COPY --chown=uws:uwsapp ./ /opt/uwsapp/pop/
RUN rm -vf /opt/uwsapp/pop/Dockerfile /opt/uwsapp/pop/.dockerignore

USER uws:uwsapp
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/pop

USER uwsapp:uwsapp
WORKDIR /opt/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENV UWSAPP_NAME pop
ENV UWSAPP_URL pop/

ENTRYPOINT /usr/local/bin/entrypoint.sh
