.PHONY: default
default: build

.PHONY: build
build:
	@./docker/base/build.sh

.PHONY: prune
prune:
	@docker system prune -f
