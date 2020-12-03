# -- ARNOLD
ARNOLD_IMAGE_NAME      ?= arnold
ARNOLD_IMAGE_TAG       ?= $(shell tr -d '\n' < VERSION)
ARNOLD_IMAGE_TAG_DEV   ?= $(ARNOLD_IMAGE_TAG)-dev
ARNOLD_IMAGE           ?= $(ARNOLD_IMAGE_NAME):$(ARNOLD_IMAGE_TAG)
ARNOLD_IMAGE_DEV       ?= $(ARNOLD_IMAGE_NAME):$(ARNOLD_IMAGE_TAG_DEV)
ANSIBLE_VAULT_PASSWORD ?= $(ARNOLD_DEFAULT_VAULT_PASSWORD)

# -- Commands
ARNOLD = \
  ARNOLD_IMAGE_NAME=$(ARNOLD_IMAGE_NAME) \
  ARNOLD_IMAGE_TAG=$(ARNOLD_IMAGE_TAG_DEV) \
  ARNOLD_IMAGE=$(ARNOLD_IMAGE_DEV) \
  ANSIBLE_VAULT_PASSWORD=$(ANSIBLE_VAULT_PASSWORD) \
  bin/arnold
ARNOLD_RUN_DEV = $(ARNOLD) -d -- run

# -- Docker
# Get the current user ID to use for docker run and docker exec commands
DOCKER_UID  = $(shell id -u)
DOCKER_GID  = $(shell id -g)
DOCKER_USER = $(DOCKER_UID):$(DOCKER_GID)

# -- k8s
K8S_DOMAIN ?= "$(shell hostname -I | awk '{print $$1}')"

# -- Linters
ANSIBLE_LINT_RULES_DIR  = /usr/local/share/ansible-lint/rules
ANSIBLE_LINT_SKIP_RULES = E602

# ==============================================================================
# RULES

default: help

# -- Docker
build: ## build Arnold's image (production)
	DOCKER_USER=$(DOCKER_USER) docker build --target=production -t $(ARNOLD_IMAGE) .
.PHONY: build

build-dev: ## build Arnold's image (development)
	DOCKER_USER=$(DOCKER_USER) docker build --target=development -t $(ARNOLD_IMAGE_DEV) .
.PHONY: build-dev

cluster: ## start a local k8s cluster for development
	oc cluster up --server-loglevel=5 --public-hostname=$(K8S_DOMAIN)
	oc login https://$(K8S_DOMAIN):8443 -u developer -p developer --insecure-skip-tls-verify=true
.PHONY: cluster

lint: ## run all linters
lint: \
  lint-ansible \
  lint-docker \
  lint-bash \
  lint-isort \
  lint-flake8 \
  lint-pylint
.PHONY: lint

lint-ansible: ## lint ansible sources
	@echo 'lint:ansible started…'
	@echo 'Checking syntax…'
	$(ARNOLD_RUN_DEV) ansible-playbook --syntax-check ./*.yml
	@echo 'Linting sources…'
	$(ARNOLD_RUN_DEV) ansible-lint -R -r $(ANSIBLE_LINT_RULES_DIR) -x $(ANSIBLE_LINT_SKIP_RULES) ./*.yml
.PHONY: lint-ansible

lint-bash: ## lint bash scripts with shellcheck
	@echo 'lint:bash started…'
	$(ARNOLD_RUN_DEV) shellcheck --shell=bash bin/*
.PHONY: lint-bash

lint-docker: ## lint Dockerfile
	@echo 'lint:docker started…'
	docker run --rm -i hadolint/hadolint < Dockerfile
.PHONY: lint-docker

lint-flake8: ## lint back-end python sources with flake8
	@echo 'lint:flake8 started…'
	$(ARNOLD_RUN_DEV) flake8 filter_plugins lookup_plugins tests
.PHONY: lint-flake8

lint-isort: ## automatically re-arrange python imports in back-end code base
	@echo 'lint:isort started…'
	$(ARNOLD_RUN_DEV) isort --diff --check-only filter_plugins lookup_plugins tests
.PHONY: lint-isort

lint-plugins: ## run python linters for plugins
lint-plugins: \
  lint-isort \
  lint-flake8 \
  lint-pylint
.PHONY: lint-plugins

lint-pylint: ## lint back-end python sources with pylint
	@echo 'lint:pylint started…'
	$(ARNOLD_RUN_DEV) pylint filter_plugins lookup_plugins tests
.PHONY: lint-pylint

status: ## get local k8s cluster status
	oc cluster status
.PHONY: status

stop: ## stop local k8s cluster
	oc cluster down
.PHONY: stop

test: ## run plugins tests
	$(ARNOLD_RUN_DEV) pytest
.PHONY: test

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

