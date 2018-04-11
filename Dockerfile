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

FROM debian:stretch

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl python-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Open Shift client
ENV OC_VERSION=v3.9.0 \
    OC_TAG_SHA=191fece

RUN curl -sLo /tmp/oc.tar.gz https://github.com/openshift/origin/releases/download/${OC_VERSION}/openshift-origin-client-tools-${OC_VERSION}-${OC_TAG_SHA}-linux-64bit.tar.gz && \
    tar xzvf /tmp/oc.tar.gz -C /tmp/ && \
    mv /tmp/openshift-origin-client-tools-${OC_VERSION}-${OC_TAG_SHA}-linux-64bit/oc /usr/local/bin/ && \
    rm -rf /tmp/oc.tar.gz /tmp/openshift-origin-client-tools-${OC_VERSION}-${OC_TAG_SHA}-linux-64bit

ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application sources in the container so that we can run all playbooks
# within the container (without volumes)
COPY . /app/

# Give the "root" group the same permissions as the "root" user on /etc/passwd
# to allow a user belonging to the root group to add new users; typically the
# docker user (see entrypoint).
RUN chmod g=u /etc/passwd
RUN chmod g=u /app

ENTRYPOINT ["/app/bin/entrypoint"]

# Un-privileged user running the application
USER 10000
