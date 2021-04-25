help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

IMG ?= pyrest
CONTAINER ?= pyrest-cnt
DB_URL_DEV ?= sqlite:////app/sql_app.db

pip_install:  ## Pip install dependencies
	pip install -r requirements.txt

build_image:  ## Build image
	docker build -t ${IMG} .

run:  ## Run image
	docker run --rm -d --name ${CONTAINER} -p 80:80 ${IMG}

run_dev:  ## Run image in dev mode
	docker run --rm  -d --name ${CONTAINER} -p 80:80 \
				--mount type=bind,source=${PWD}/app,target=/app \
				--env DB_URL=${DB_URL_DEV} \
				${IMG} uvicorn main:app --host 0.0.0.0 --port 80 --reload

stop:  ## Stop container
	-docker stop ${CONTAINER} || true

build_run_dev: build_image stop run_dev  ## Build image and run it in dev mode
	@echo 'done'

bash:  ## Access container with bash
	docker exec -it ${CONTAINER} bash

