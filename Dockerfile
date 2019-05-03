# This Dockerfile is part of the Arnold project. It is used to run Arnold's
# Ansible playbooks for the CI/CD of FUN's infrastructure. These playbooks can
# be run either:
#
# - by developpers on their laptops for configuration (e.g. adding a new
#   customer to the infrastructure),
# - by GitLab for CI/CD operations,
#
# In order to run this container, you will need to provide the following
# environment variables:
#
# - ANSIBLE_VAULT_PASS: used to decrypt vaulted content
# - K8S_AUTH_API_KEY: K8S service account token (required to run ansible k8s plugin)
# - K8S_AUTH_HOST: K8S API host (e.g. https://192.168.1.1:6550)
#
# Optionally, you can pass the following environment variable :
#
# - K8S_AUTH_SSL_CA_CERT_B64 : A base64 encoded CA certificate to authenticate
#   against the K8S API (see ca_cert option in ansible k8s plugin)

FROM python:3.9-slim as base

# Upgrade pip to its latest release to speed up dependencies installation
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip

# -- Builder --
FROM base as builder

WORKDIR /build

COPY requirements/production.txt /build/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


# -- Core --
FROM base as core

# hadolint ignore=DL3015,DL3008
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

WORKDIR /app

COPY . /app/

COPY bin/vault-password /usr/local/bin/vault-password
ENV ANSIBLE_VAULT_PASSWORD_FILE=/usr/local/bin/vault-password

# Give the "root" group the same permissions as the "root" user on /etc/passwd
# to allow a user belonging to the root group to add new users; typically the
# docker user (see entrypoint). And also allow the root group to create files in
# /home/arnold that is the running-user's home directory.
RUN chmod g=u /etc/passwd && \
    mkdir /home/arnold && \
    chmod g=u /home/arnold

ENTRYPOINT ["/app/bin/entrypoint"]


# -- Development --
FROM core as development

# hadolint ignore=DL3015,DL3008
RUN apt-get update && \
    apt-get install -y \
      curl \
      jq \
      shellcheck \
      unzip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements/development.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# pylint history and cache files
ENV PYLINTHOME="/app/.pylint.d"

# Copy the application sources in the container so that we can run all playbooks
# within the container (without volumes)
COPY . /app/

# Un-privileged user running the application
USER ${DOCKER_USER:-1000}


# -- Production --
FROM core as production

# Un-privileged user running the application
USER ${DOCKER_USER:-1000}
