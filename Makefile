help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

IMG = pyrest
CONTAINER = pyrest-cnt
DB_URL_DEV ?= sqlite:////app/sql_app.db
OPENAPI_JSON = openapi.json

clear:  ## Delete all unused cache an files
	-find . -name __pycache__ | xargs rm -rf
	-find . -name .pytest_cache | xargs rm -rf
	-find . -name .coverage | xargs rm -rf

pip_install:  ## Pip install dependencies
	pip install -r requirements.txt

build_image:  ## Build image
	docker build -t ${IMG} .

run:  ## Run image
	docker run --rm -d --name ${CONTAINER} -p 80:80 ${IMG}

run_dev:  ## Run image in dev mode
	docker run --rm  -d --name ${CONTAINER} -p 80:80 \
				--mount type=bind,source=${PWD}/app,target=/app \
				--mount type=bind,source=${PWD}/tests,target=/tests \
				--env DB_URL=${DB_URL_DEV} \
				${IMG} uvicorn main:app --host 0.0.0.0 --port 80 --reload

stop:  ## Stop container
	-@docker stop ${CONTAINER}

build_run_dev: build_image stop run_dev  ## Build image and run it in dev mode
	@echo 'running in dev mode'

bash:  ## Access container with bash
	docker exec -it ${CONTAINER} bash

test:  ## Run test
	docker run --rm ${IMG} py.test -vv --cov=/app --cov-report term-missing /tests

get_api_doc:  ## Get openapi.json (assume service is already running locally)
	curl http://localhost/openapi.json | jq . > ${OPENAPI_JSON}
