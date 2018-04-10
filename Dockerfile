# This Dockerfile is part of the Arnold project. It is used to run Arnold's
# Ansible playbooks for the CI/CD of FUN's infrastructure. These playbooks can
# be run either:
#
# - by developpers on their laptops for configuration (e.g. adding a new
#   customer to the infrastructure),
# - by GitLab for CI/CD operations,
# - by OpenShift in init containers.
#
FROM debian:stretch

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y curl python-pip sudo && \
    rm -rf /var/lib/apt/lists/*

ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./ansible.cfg /app/

# Install Open Shift client
ENV OC_VERSION=v3.9.0 \
    OC_TAG_SHA=191fece

RUN curl -sLo /tmp/oc.tar.gz https://github.com/openshift/origin/releases/download/${OC_VERSION}/openshift-origin-client-tools-${OC_VERSION}-${OC_TAG_SHA}-linux-64bit.tar.gz && \
    tar xzvf /tmp/oc.tar.gz -C /tmp/ && \
    mv /tmp/openshift-origin-client-tools-${OC_VERSION}-${OC_TAG_SHA}-linux-64bit/oc /usr/local/bin/ && \
    rm -rf /tmp/oc.tar.gz /tmp/openshift-origin-client-tools-${OC_VERSION}-${OC_TAG_SHA}-linux-64bit

ADD ./.vault_pass.sh /app/
RUN chmod +x /app/.vault_pass.sh

ADD ./bin/entrypoint /app/bin/

RUN echo "ALL ALL=NOPASSWD: ALL" > /etc/sudoers.d/usermod
RUN chmod 666 /etc/passwd

ENTRYPOINT ["/app/bin/entrypoint"]
