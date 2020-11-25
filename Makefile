# -- ARNOLD
ARNOLD_IMAGE_NAME = arnold
ARNOLD_IMAGE_TAG  = $(shell tr -d '\n' < VERSION)

# -- Docker
# Get the current user ID to use for docker run and docker exec commands
DOCKER_UID  = $(shell id -u)
DOCKER_GID  = $(shell id -g)
DOCKER_USER = $(DOCKER_UID):$(DOCKER_GID)

# ==============================================================================
# RULES

default: help

# -- Docker
build: ## build Arnold's image (production)
	DOCKER_USER=$(DOCKER_USER) docker build --target=production -t $(ARNOLD_IMAGE_NAME):$(ARNOLD_IMAGE_TAG) .
.PHONY: build

build-dev: ## build Arnold's image (development)
	DOCKER_USER=$(DOCKER_USER) docker build --target=development -t $(ARNOLD_IMAGE_NAME):$(ARNOLD_IMAGE_TAG)-dev .
.PHONY: build-dev

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

