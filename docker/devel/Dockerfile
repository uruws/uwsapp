FROM uwsapp/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220523"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh less shellcheck python3-doc \
	python3-coverage mypy

USER uws:uws

ENV USER uws
ENV HOME /home/uws
ENV UWSAPP_DEBUG on

WORKDIR ${UWSAPP_HOME}
ENTRYPOINT /usr/local/bin/uws-login.sh
