# Load defaults
include bin/_defaults

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

# -- Files
PLAYBOOKS = $(filter-out dependencies.yml registry.yml, $(wildcard *.yml))

# -- Docker
# Get the current user ID to use for docker run and docker exec commands
DOCKER_UID  = $(shell id -u)
DOCKER_GID  = $(shell id -g)
DOCKER_USER = $(DOCKER_UID):$(DOCKER_GID)

# -- k8s
K8S_DOMAIN ?= "$(shell hostname -I | awk '{print $$1}')"
K3D_CLUSTER_NAME ?= arnold

# -- Linters
ANSIBLE_LINT_SKIP_RULES = experimental

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

cluster: ## start a local k8s cluster for development (with k3d)
	@bin/init-cluster "$(K3D_CLUSTER_NAME)"
.PHONY: cluster

lint: ## run all linters
lint: \
  lint-ansible \
  lint-docker \
  lint-bash \
  lint-plugins
.PHONY: lint

lint-ansible: ## lint ansible sources
	@echo 'lint:ansible started…'
	@echo 'Checking syntax…'
	$(ARNOLD_RUN_DEV) ansible-playbook --syntax-check $(PLAYBOOKS)
	@echo 'Linting sources…'
	$(ARNOLD_RUN_DEV) ansible-lint -R -x $(ANSIBLE_LINT_SKIP_RULES) $(PLAYBOOKS)
.PHONY: lint-ansible

lint-bash: ## lint bash scripts with shellcheck
	@echo 'lint:bash started…'
	$(ARNOLD_RUN_DEV) shellcheck -x --shell=bash bin/*
.PHONY: lint-bash

lint-black: ## lint back-end python sources with Black
	@echo 'lint:black started…'
	$(ARNOLD_RUN_DEV) black --check filter_plugins lookup_plugins tests
.PHONY: lint-black

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
  lint-black \
  lint-isort \
  lint-flake8 \
  lint-pylint
.PHONY: lint-plugins

lint-pylint: ## lint back-end python sources with pylint
	@echo 'lint:pylint started…'
	$(ARNOLD_RUN_DEV) pylint filter_plugins lookup_plugins tests
.PHONY: lint-pylint

status: ## get local k8s cluster status
	k3d cluster list "$(K3D_CLUSTER_NAME)"
.PHONY: status

stop: ## stop local k8s cluster
	k3d cluster stop "$(K3D_CLUSTER_NAME)"
.PHONY: stop

test: ## run plugins tests
	$(ARNOLD_RUN_DEV) pytest
.PHONY: test

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

