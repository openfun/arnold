# This Dockerfile is part of the Arnold project. It is used to run Arnold's Ansible playbooks
# for the CI/CD of FUN's infrastructure. These playbooks can be run either:
#
# - by developpers on their laptops for configuration (e.g. adding a new customer to the
#   infrastructure),
# - by GitLab for CI/CD operations,
# - by OpenShift in init containers.
#
FROM debian:stretch

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python-pip sudo && \
    rm -rf /var/lib/apt/lists/*

ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./ansible.cfg /app/

ADD ./.vault_pass.sh /app/
RUN chmod +x /app/.vault_pass.sh

ADD ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN echo "ALL ALL=NOPASSWD: ALL" > /etc/sudoers.d/usermod
RUN chmod 666 /etc/passwd

ENTRYPOINT ["/entrypoint.sh"]
