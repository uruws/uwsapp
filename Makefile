.PHONY: default
default: build

.PHONY: build
build:
	@./docker/base/build.sh
	@./docker/devel/build.sh
	@./core/build.sh
	@./api/build.sh
	@./web/build.sh

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
	@docker system prune -f

.PHONY: check
check:
	@./docker/devel/check.sh
