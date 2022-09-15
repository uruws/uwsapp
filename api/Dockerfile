FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220915"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh openssh-client

RUN install -v -d -o uws -g uwsapp -m 0750 /run/uwsapi \
	&& install -v -d -o uws -g uwsapp -m 0750 /run/uwscli \
	&& install -v -d -o uws -g uwsapp -m 0750 /run/uwscli/auth \
	&& install -v -d -o uws -g uwsapp -m 0750 /run/uwscli/logs

RUN install -v -d -o uws -g uwsapp -m 0750 /opt/uwsapp/api
COPY --chown=uws:uwsapp ./ /opt/uwsapp/api/
RUN rm -vf /opt/uwsapp/api/Dockerfile /opt/uwsapp/api/.dockerignore

USER uws:uwsapp
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/api

USER uwsapp:uwsapp
WORKDIR /opt/uwsapp

ENV USER uwsapp
ENV HOME /home/uwsapp

ENV UWSAPP_NAME api
ENV UWSAPP_URL api/

ENTRYPOINT /usr/local/bin/entrypoint.sh
