FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsapp -m 0750 /run/uwsSKEL

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp/SKEL
COPY --chown=uws:uwsapp ./ /opt/uwsapp/SKEL/
RUN rm -vf /opt/uwsapp/SKEL/Dockerfile /opt/uwsapp/SKEL/.dockerignore

USER uws:uwsapp
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/SKEL

USER uwsapp:uwsapp
WORKDIR /opt/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENV UWSAPP_NAME SKEL
ENV UWSAPP_URL SKEL/

ENTRYPOINT /usr/local/bin/entrypoint.sh
