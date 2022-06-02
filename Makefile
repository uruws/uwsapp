.PHONY: default
default: build

.PHONY: all
all: build devel

.PHONY: build
build:
	@./docker/base/build.sh

.PHONY: devel
devel: nginx
	@./docker/devel/build.sh

.PHONY: nginx
nginx:
	@./docker/nginx/build.sh

.PHONY: prune
prune:
	@docker system prune -f
