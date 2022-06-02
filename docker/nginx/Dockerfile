FROM uws/mkcert-2203

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220602"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh less ssl-cert nginx

RUN rm -vf /etc/nginx/sites-enabled/default
COPY --chown=root:root ./etc/devel.conf /etc/nginx/sites-enabled/default

COPY --chown=root:root ./etc/devel-ssl.conf /etc/nginx/sites-enabled/default-ssl

COPY --chown=root:root ./bin/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod -v 0555 /usr/local/bin/entrypoint.sh

RUN install -v -d -m 0755 -o root -g root /var/tmp/nginx
RUN /usr/sbin/nginx -t

ENTRYPOINT /usr/local/bin/entrypoint.sh
