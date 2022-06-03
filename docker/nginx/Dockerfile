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

ENV CAROOT /usr/local/etc/ca

RUN install -v -d -m 0755 -o root -g root /usr/local/etc/ssl
COPY --chown=root:root ./etc/openssl.cnf /usr/local/etc/ssl/openssl.cnf

RUN install -v -d -m 0750 -o root -g root /usr/local/etc/ca
RUN install -v -d -m 0750 -o root -g root /usr/local/etc/ca/client
RUN install -v -d -m 0750 -o root -g root /usr/local/etc/ca/cert

RUN echo '5946eae9-e236-5a12-8b59-0b94b112f6a1:supersecret' >/usr/local/etc/ca/client.pw

RUN echo 1000 >/usr/local/etc/ca/serial
RUN echo 1000 >/usr/local/etc/ca/crlnumber
RUN touch /usr/local/etc/ca/index.txt
RUN touch /usr/local/etc/ca/index.txt.attr

RUN HOME=/usr/local/etc /usr/local/bin/ca-client.sh devel@uwsapp.local
RUN HOME=/usr/local/etc /usr/local/bin/ca-cert.sh uwsapp.local

RUN /usr/sbin/nginx -t
ENTRYPOINT /usr/local/bin/entrypoint.sh
