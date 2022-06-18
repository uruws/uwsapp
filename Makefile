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

.PHONY: clean
clean:
	@find . -type d -name __pycache__ | xargs rm -fr
	@rm -f .coverage

.PHONY: distclean
distclean: clean
	@rm -rf ./data ./run ./tmp

.PHONY: prune
prune:
	@docker system prune -f

.PHONY: check
check:
	@./docker/devel/check.sh
