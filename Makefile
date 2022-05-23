.PHONY: default
default: build

.PHONY: all
all: build devel

.PHONY: build
build:
	@./docker/base/build.sh

.PHONY: devel
devel:
	@./docker/devel/build.sh

.PHONY: prune
prune:
	@docker system prune -f
