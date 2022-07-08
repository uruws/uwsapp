.PHONY: default
default: build

.PHONY: build
build:
	@./docker/base/build.sh
	@./docker/devel/build.sh
	@./core/build.sh
	@./api/build.sh
	@./web/build.sh
#~ 	@./pop/build.sh

.PHONY: devel
devel:
	@./docker/base/build.sh
	@./docker/nginx/build.sh
	@./docker/devel/build.sh

.PHONY: clean
clean:
	@find . -type d -name __pycache__ | xargs rm -fr
	@rm -f .coverage

.PHONY: distclean
distclean: clean
	@rm -rf ./data ./run ./tmp

.PHONY: prune
prune:
	@docker rmi uwsapp/pop || true
	@docker system prune -f

.PHONY: check
check:
	@./docker/devel/check.sh

UWSAPP_VERSION != cat ./VERSION

.PHONY: publish
publish:
	@$(MAKE) -C /srv/uws/deploy ./docker/ecr-login.sh us-west-1
	@$(MAKE) -C /srv/uws/deploy ./cluster/ecr-push.sh us-west-1 \
		uwsapp/api uws:uwsapi-$(UWSAPP_VERSION)
	@$(MAKE) -C /srv/uws/deploy ./cluster/ecr-push.sh us-west-1 \
		uwsapp/web uws:uwsweb-$(UWSAPP_VERSION)
