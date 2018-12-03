# This Dockerfile is part of the Arnold project. It is used to run Arnold's
# Ansible playbooks for the CI/CD of FUN's infrastructure. These playbooks can
# be run either:
#
# - by developpers on their laptops for configuration (e.g. adding a new
#   customer to the infrastructure),
# - by GitLab for CI/CD operations,
# - by OpenShift in init containers.
#
# In order to run this container, you will need to provide the following
# environment variables:
#
# - ANSIBLE_VAULT_PASS: used to decrypt vaulted content
# - K8S_AUTH_API_KEY: OpenShift user's API token (required to run oc commands)
# - K8S_AUTH_HOST: OpenShift's console url (e.g. https://openshift.startup.com:8443)

FROM python:3.6

WORKDIR /app

# hadolint ignore=DL3015,DL3008
RUN apt-get update && \
    apt-get install -y \
    shellcheck \
    unzip && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements/pip-requirements.txt /app/requirements/
RUN pip install -r /app/requirements/pip-requirements.txt

# Install more ansible_lint_rules
ENV ANSIBLE_LINT_RULES_DIR="/tmp/_ansible_lint_rules"

RUN mkdir -p "${ANSIBLE_LINT_RULES_DIR}" && \
    curl -sLo /tmp/ansible-lint-rules.zip https://github.com/tsukinowasha/ansible-lint-rules/archive/master.zip && \
    unzip -j /tmp/ansible-lint-rules.zip  '*/rules/*' -d "${ANSIBLE_LINT_RULES_DIR}" && \
    rm -rf "/tmp/ansible-lint-rules.zip"

# Copy the application sources in the container so that we can run all playbooks
# within the container (without volumes)
COPY . /app/

# Give the "root" group the same permissions as the "root" user on /etc/passwd
# to allow a user belonging to the root group to add new users; typically the
# docker user (see entrypoint). And also allow the root group to create files in
# /home/arnold that is the running-user's home directory.
RUN chmod g=u /etc/passwd && \
    mkdir /home/arnold && \
    chmod g=u /home/arnold

ENTRYPOINT ["/app/bin/entrypoint"]

# Un-privileged user running the application
USER 10000
