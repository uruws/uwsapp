FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220523"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh python3 uwsgi-plugin-python3 \
	sqlite3 python3-django

RUN install -v -d -o uws -g uwsops -m 0750 /opt/uws

USER uwsops:uwsops

ENV USER uwsops
ENV HOME /home/uwsops

ENV UWSAPP_HOME /opt/uws
ENV UWSAPP_PORT 3000
ENV UWSAPP_WORKERS 3

USER uws:uws

ENV USER uws
ENV HOME /home/uws

ENV UWSAPP_HOME /opt/uws
ENV UWSAPP_PORT 3000
ENV UWSAPP_WORKERS 3

COPY --chown=uws:uwsops ./bin/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod -v 0750  /usr/local/bin/entrypoint.sh

WORKDIR /opt/uws
ENTRYPOINT /usr/local/bin/entrypoint.sh
