FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220617"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsops -m 0750 /opt/uwsapp/SKEL
COPY --chown=uws:uwsops ./ /opt/uwsapp/SKEL/
RUN rm -vf /opt/uwsapp/SKEL/Dockerfile /opt/uwsapp/SKEL/.dockerignore

USER uws:uwsops

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/SKEL

ENV UWSAPP_NAME SKEL

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/local/bin/entrypoint.sh
