help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

build_image:  ## Build image
	docker build -t exp-fastapi .

run_fastapi:  ## Run fastapi image
	docker run --rm -d --name container-fastapi -p 80:80 exp-fastapi
