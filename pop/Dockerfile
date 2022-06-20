FROM uwsapp/core

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220620"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uwsops -m 0750 /opt/uwsapp/pop
COPY --chown=uws:uwsops ./ /opt/uwsapp/pop/
RUN rm -vf /opt/uwsapp/pop/Dockerfile /opt/uwsapp/pop/.dockerignore

USER uws:uwsops

ENV USER uws
ENV HOME /home/uws

RUN python3 --version \
	&& python3 -m compileall /opt/uwsapp/pop

ENV UWSAPP_NAME pop

WORKDIR /opt/uwsapp
ENTRYPOINT /usr/local/bin/entrypoint.sh
