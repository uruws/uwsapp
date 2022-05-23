.PHONY: default
default: build

.PHONY: build
build:
	@./docker/build.sh

.PHONY: prune
prune:
	@docker system prune -f
